from __future__ import annotations

import json
import hashlib
import math
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

from .project import load_project, project_path, save_project, update_step


AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}
FONT_CANDIDATES = (
    Path("/System/Library/Fonts/AppleSDGothicNeo.ttc"),
    Path("/System/Library/Fonts/Supplemental/AppleGothic.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
)


class ProductionError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        retryable: bool = True,
        action: str = "문제를 확인한 뒤 실패 단계부터 다시 시도해 주세요.",
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.action = action


def resolve_font_path() -> Path:
    for path in FONT_CANDIDATES:
        if path.exists():
            return path
    raise ProductionError(
        "Cover에 사용할 한글 글꼴을 찾을 수 없습니다.",
        action="macOS 기본 글꼴을 확인하거나 프로그램을 다시 설치해 주세요.",
    )


def asset_signature(tracks: list[Path], image: Path) -> str:
    digest = hashlib.sha256()
    for path in [*tracks, image]:
        digest.update(path.name.encode("utf-8"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def step_status(manifest: dict, step_id: str) -> str | None:
    return next(
        (step.get("status") for step in manifest["steps"] if step.get("id") == step_id),
        None,
    )


def invalidate_generated_steps(manifest: dict) -> None:
    generated_ids = {
        "cover",
        "audio_analysis",
        "audio_assembly",
        "video_render",
        "metadata",
        "quality_check",
        "output_ready",
    }
    for step in manifest["steps"]:
        if step.get("id") in generated_ids:
            step["status"] = "pending"
    manifest["validation"] = None
    manifest["output"] = None


def clear_audio_cache(audio_work_dir: Path) -> None:
    if not audio_work_dir.exists():
        return
    for path in audio_work_dir.glob("*.m4a"):
        path.unlink()
    (audio_work_dir / "playlist.txt").unlink(missing_ok=True)


def ensure_disk_space(path: Path, duration_seconds: float) -> None:
    free_bytes = shutil.disk_usage(path).free
    estimated_bytes = max(1_000_000_000, int(duration_seconds * 100_000))
    required_bytes = estimated_bytes + 512_000_000
    if free_bytes < required_bytes:
        free_gb = free_bytes / 1_000_000_000
        required_gb = required_bytes / 1_000_000_000
        raise ProductionError(
            f"저장 공간이 부족합니다. 사용 가능 {free_gb:.1f}GB, 필요 약 {required_gb:.1f}GB.",
            action="디스크 공간을 확보한 뒤 실패 단계부터 다시 시도해 주세요.",
        )


def run_command(arguments: list[str], log_path: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(arguments, capture_output=True, text=True, check=False)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(arguments) + "\n")
        handle.write(result.stdout)
        handle.write(result.stderr)
        handle.write("\n")
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        tail = detail[-1] if detail else "알 수 없는 실행 오류"
        raise ProductionError(f"미디어 처리에 실패했습니다: {tail}")
    return result


def discover_assets(project_id: str) -> tuple[list[Path], Path]:
    root = project_path(project_id)
    tracks = sorted(
        path
        for path in (root / "work" / "tracks").iterdir()
        if path.is_file() and path.suffix.lower() in AUDIO_EXTENSIONS
    )
    images = sorted(
        path
        for path in (root / "work" / "image").iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    if not tracks:
        raise ProductionError("work/tracks 폴더에 음악 파일이 없습니다.")
    if not images:
        raise ProductionError("work/image 폴더에 대표 이미지가 없습니다.")
    return tracks, images[0]


def probe_duration(path: Path, log_path: Path) -> float:
    result = run_command(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(path),
        ],
        log_path,
    )
    try:
        duration = float(result.stdout.strip())
    except ValueError as error:
        raise ProductionError(f"재생시간을 읽을 수 없습니다: {path.name}") from error
    if not math.isfinite(duration) or duration <= 0:
        raise ProductionError(f"유효하지 않은 음악 파일입니다: {path.name}")
    return duration


def format_timestamp(seconds: float) -> str:
    total = max(0, int(round(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def wrap_title(
    draw: ImageDraw.ImageDraw,
    title: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    units = title.split() if " " in title else list(title)
    separator = " " if " " in title else ""
    lines: list[str] = []
    current = ""
    for unit in units:
        candidate = (current + separator + unit).strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = unit
    if current:
        lines.append(current)
    return lines


def fit_title(
    draw: ImageDraw.ImageDraw,
    title: str,
    max_width: int,
    font_path: Path,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(76, 35, -2):
        font = ImageFont.truetype(str(font_path), size=size)
        lines = wrap_title(draw, title, font, max_width)
        if len(lines) <= 2 and all(
            draw.textbbox((0, 0), line, font=font)[2] <= max_width for line in lines
        ):
            return font, lines
    font = ImageFont.truetype(str(font_path), size=36)
    return font, wrap_title(draw, title, font, max_width)[:2]


def create_cover(source: Path, destination: Path, theme: str) -> None:
    font_path = resolve_font_path()
    with Image.open(source) as image:
        base = ImageOps.fit(image.convert("RGB"), (1920, 1080), method=Image.Resampling.LANCZOS)
    base = ImageEnhance.Contrast(base).enhance(1.04)
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 650, 1920, 1080), fill=(5, 8, 13, 118))
    composed = Image.alpha_composite(base.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(composed)
    font, lines = fit_title(draw, theme, 1460, font_path)
    subtitle_font = ImageFont.truetype(str(font_path), size=31)
    y = 760
    for line in lines[:2]:
        draw.text((150, y), line, font=font, fill=(249, 245, 235, 255))
        y += font.size + 12
    draw.text(
        (153, y + 14), "RELAXING JAZZ · LONG PLAY",
        font=subtitle_font, fill=(220, 188, 117, 255),
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    composed.convert("RGB").save(destination, "JPEG", quality=94, optimize=True)


def normalize_tracks(
    tracks: list[Path], audio_work_dir: Path, log_path: Path
) -> list[Path]:
    normalized: list[Path] = []
    audio_work_dir.mkdir(parents=True, exist_ok=True)
    for index, source in enumerate(tracks, start=1):
        destination = audio_work_dir / f"{index:02d}.m4a"
        if not destination.exists() or destination.stat().st_mtime < source.stat().st_mtime:
            temporary = destination.with_suffix(".tmp.m4a")
            temporary.unlink(missing_ok=True)
            run_command(
                [
                    "ffmpeg", "-y", "-i", str(source), "-vn", "-c:a", "aac",
                    "-b:a", "320k", "-ar", "48000", "-ac", "2", str(temporary),
                ],
                log_path,
            )
            temporary.replace(destination)
        normalized.append(destination)
    return normalized


def write_concat_file(paths: list[Path], destination: Path, repeat_count: int) -> None:
    lines: list[str] = []
    for _ in range(repeat_count):
        for path in paths:
            escaped = str(path.resolve()).replace("'", "'\\''")
            lines.append(f"file '{escaped}'")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_video(
    cover: Path,
    normalized: list[Path],
    repeat_count: int,
    destination: Path,
    work_dir: Path,
    log_path: Path,
) -> None:
    concat_file = work_dir / "playlist.txt"
    full_mix = work_dir / "Full_Mix.m4a"
    write_concat_file(normalized, concat_file, repeat_count)
    run_command(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c", "copy", str(full_mix),
        ],
        log_path,
    )
    run_command(
        [
            "ffmpeg", "-y", "-loop", "1", "-framerate", "24", "-i", str(cover),
            "-i", str(full_mix), "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage",
            "-crf", "20", "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(destination),
        ],
        log_path,
    )


def write_metadata(output_dir: Path, theme: str, chapters: list[dict], total: float) -> None:
    chapter_lines = [
        f"{format_timestamp(item['start'])} {item['title']}" for item in chapters
    ]
    title = f"{theme} | Relaxing Jazz for Sleep, Study & Night"
    if len(title) > 100:
        title = title[:97].rstrip() + "..."
    description = (
        f"{theme}\n\n"
        "조용히 쉬거나 집중할 때 함께할 수 있는 긴 호흡의 재즈 플레이리스트입니다.\n"
        "전체 곡 세트는 세 번 반복됩니다.\n\n"
        "Track list\n"
        + "\n".join(chapter_lines)
        + "\n\n#Jazz #RelaxingJazz #SeoulJazz #StudyMusic #SleepMusic\n"
    )
    (output_dir / "Title.txt").write_text(title + "\n", encoding="utf-8")
    (output_dir / "Description.txt").write_text(description, encoding="utf-8")
    (output_dir / "Chapters.txt").write_text(
        "\n".join(chapter_lines) + "\n", encoding="utf-8"
    )
    (output_dir / "Upload_Info.txt").write_text(
        "UPLOAD PACKAGE\n"
        f"Title: {title}\n"
        f"Total duration: {format_timestamp(total)}\n"
        "Video: 1920x1080, 24fps, H.264\n"
        "Audio: AAC, 48kHz, stereo, 320kbps target\n"
        "Thumbnail: Cover.jpg (영상 고정 이미지와 동일)\n"
        "Upload: YouTube Studio에서 직접 진행\n",
        encoding="utf-8",
    )


def validate_video(path: Path, expected_duration: float, log_path: Path) -> dict:
    result = run_command(
        [
            "ffprobe", "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(path),
        ],
        log_path,
    )
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    audio = next((item for item in streams if item.get("codec_type") == "audio"), None)
    duration = float(data.get("format", {}).get("duration", 0))
    frame_rate_value = (video or {}).get("avg_frame_rate") or (video or {}).get("r_frame_rate")
    try:
        frame_rate = float(Fraction(frame_rate_value))
    except (TypeError, ValueError, ZeroDivisionError):
        frame_rate = 0.0
    checks = {
        "videoCodec": video and video.get("codec_name") == "h264",
        "resolution": video and video.get("width") == 1920 and video.get("height") == 1080,
        "frameRate": abs(frame_rate - 24.0) < 0.01,
        "audioCodec": audio and audio.get("codec_name") == "aac",
        "stereo": audio and int(audio.get("channels", 0)) == 2,
        "duration": abs(duration - expected_duration) < max(3.0, expected_duration * 0.002),
    }
    return {
        "passed": all(bool(value) for value in checks.values()),
        "checks": checks,
        "durationSeconds": duration,
    }


def analyze_tracks(
    manifest: dict,
    tracks: list[Path],
    log_path: Path,
) -> tuple[list[dict], float]:
    planned = manifest.get("tracks", [])
    chapters: list[dict] = []
    elapsed = 0.0
    for index, path in enumerate(tracks, start=1):
        duration = probe_duration(path, log_path)
        title = planned[index - 1]["title"] if index <= len(planned) else path.stem
        chapters.append(
            {"index": index, "title": title, "start": elapsed, "duration": duration}
        )
        elapsed += duration
    manifest["tracks"] = [
        {
            "index": item["index"],
            "title": item["title"],
            "prompt": planned[item["index"] - 1].get("prompt", "")
            if item["index"] <= len(planned)
            else "",
            "status": "ready",
            "sourcePath": str(tracks[item["index"] - 1]),
            "durationSeconds": item["duration"],
            "chapterStartSeconds": item["start"],
        }
        for item in chapters
    ]
    return chapters, elapsed


def reuse_track_analysis(manifest: dict, tracks: list[Path]) -> tuple[list[dict], float] | None:
    saved_tracks = manifest.get("tracks", [])
    if step_status(manifest, "audio_analysis") != "completed":
        return None
    if len(saved_tracks) != len(tracks):
        return None
    chapters: list[dict] = []
    for saved, source in zip(saved_tracks, tracks):
        if not saved.get("durationSeconds") or Path(saved.get("sourcePath", "")) != source:
            return None
        chapters.append(
            {
                "index": saved["index"],
                "title": saved["title"],
                "start": saved["chapterStartSeconds"],
                "duration": saved["durationSeconds"],
            }
        )
    return chapters, sum(item["duration"] for item in chapters)


def metadata_ready(output: Path, tracks: list[Path]) -> bool:
    required = (
        output / "Title.txt",
        output / "Description.txt",
        output / "Chapters.txt",
        output / "Upload_Info.txt",
    )
    generated = output / "Generated_Tracks"
    return (
        all(path.exists() and path.stat().st_size > 0 for path in required)
        and generated.is_dir()
        and all((generated / source.name).exists() for source in tracks)
    )


def record_failure(project_id: str, error: Exception) -> None:
    manifest = load_project(project_id)
    current_step = manifest.get("currentStep", "unknown")
    for step in manifest["steps"]:
        if step.get("id") == current_step and step.get("status") == "running":
            step["status"] = "failed"
    retryable = error.retryable if isinstance(error, ProductionError) else True
    action = (
        error.action
        if isinstance(error, ProductionError)
        else "production.log를 확인한 뒤 프로그램을 다시 실행해 주세요."
    )
    manifest["status"] = "failed"
    manifest["error"] = {
        "step": current_step,
        "message": str(error),
        "retryable": retryable,
        "action": action,
    }
    manifest["message"] = str(error)
    save_project(manifest)


def produce_project(project_id: str) -> None:
    manifest = load_project(project_id)
    root = project_path(project_id)
    output = root / "output"
    log_path = root / "logs" / "production.log"
    try:
        tracks, image = discover_assets(project_id)
        signature = asset_signature(tracks, image)
        generated_was_completed = any(
            step.get("id") not in {"theme_plan", "music_plan", "manual_assets"}
            and step.get("status") == "completed"
            for step in manifest["steps"]
        )
        if manifest.get("assetSignature") != signature and generated_was_completed:
            invalidate_generated_steps(manifest)
            clear_audio_cache(root / "work" / "audio")
        manifest["assetSignature"] = signature
        update_step(manifest, "manual_assets", "completed", "음악과 이미지를 확인했습니다.", 30)

        cover = output / "Cover.jpg"
        if step_status(manifest, "cover") != "completed" or not cover.exists():
            update_step(manifest, "cover", "running", "대표 이미지를 영상 규격으로 만드는 중입니다.", 35)
            create_cover(image, cover, manifest["theme"])
            update_step(manifest, "cover", "completed", "Cover.jpg를 만들었습니다.", 42)

        reused_analysis = reuse_track_analysis(manifest, tracks)
        if reused_analysis is None:
            update_step(manifest, "audio_analysis", "running", "음악 길이와 챕터를 계산하는 중입니다.", 46)
            chapters, elapsed = analyze_tracks(manifest, tracks, log_path)
            update_step(manifest, "audio_analysis", "completed", "챕터 계산을 완료했습니다.", 54)
        else:
            chapters, elapsed = reused_analysis

        audio_work = root / "work" / "audio"
        normalized = [audio_work / f"{index:02d}.m4a" for index in range(1, len(tracks) + 1)]
        audio_ready = all(path.exists() and path.stat().st_size > 0 for path in normalized)
        if step_status(manifest, "audio_assembly") != "completed" or not audio_ready:
            update_step(manifest, "audio_assembly", "running", "음악을 정규화하고 세 번 반복하는 중입니다.", 58)
            normalized = normalize_tracks(tracks, audio_work, log_path)
            update_step(manifest, "audio_assembly", "completed", "음악 세트 반복 구성을 완료했습니다.", 68)

        expected_total = elapsed * manifest["repeatCount"]
        final_video = output / "YouTube_Final.mp4"
        video_ready = final_video.exists() and final_video.stat().st_size > 0
        if step_status(manifest, "video_render") != "completed" or not video_ready:
            ensure_disk_space(output, expected_total)
            update_step(manifest, "video_render", "running", "최종 영상을 렌더링하는 중입니다.", 72)
            render_video(
                cover, normalized, manifest["repeatCount"], final_video, audio_work, log_path
            )
            update_step(manifest, "video_render", "completed", "최종 영상을 만들었습니다.", 88)

        if step_status(manifest, "metadata") != "completed" or not metadata_ready(output, tracks):
            update_step(manifest, "metadata", "running", "제목, 설명과 챕터를 만드는 중입니다.", 90)
            write_metadata(output, manifest["theme"], chapters, expected_total)
            generated_tracks = output / "Generated_Tracks"
            generated_tracks.mkdir(exist_ok=True)
            current_names = {source.name for source in tracks}
            for existing in generated_tracks.iterdir():
                if existing.is_file() and existing.name not in current_names:
                    existing.unlink()
            for source in tracks:
                shutil.copy2(source, generated_tracks / source.name)
            update_step(manifest, "metadata", "completed", "업로드 문구를 만들었습니다.", 94)

        validation = manifest.get("validation")
        if step_status(manifest, "quality_check") != "completed" or not (validation or {}).get("passed"):
            update_step(manifest, "quality_check", "running", "영상 규격을 검사하는 중입니다.", 96)
            validation = validate_video(final_video, expected_total, log_path)
            manifest["validation"] = validation
            if not validation["passed"]:
                raise ProductionError("완성 영상의 규격 검사에 실패했습니다.")
            update_step(manifest, "quality_check", "completed", "모든 영상 규격 검사를 통과했습니다.", 99)

        manifest["output"] = {
            "directory": str(output),
            "video": str(final_video),
            "cover": str(cover),
            "files": [
                "YouTube_Final.mp4", "Cover.jpg", "Title.txt", "Description.txt",
                "Chapters.txt", "Upload_Info.txt", "Generated_Tracks",
            ],
        }
        manifest["status"] = "completed"
        update_step(manifest, "output_ready", "completed", "YouTube 업로드용 결과물이 완성되었습니다.", 100)
    except Exception as error:
        record_failure(project_id, error)
