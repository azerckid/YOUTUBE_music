from __future__ import annotations

import hashlib
import re
from datetime import datetime
from pathlib import Path


TRACK_TITLES = (
    "Opening Glow",
    "Quiet Window",
    "Velvet Street",
    "After Midnight",
    "Slow Reflections",
    "City in Blue",
    "Last Table",
    "Morning Haze",
)


def safe_project_id(theme: str, now: datetime | None = None) -> str:
    timestamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    latin = re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-")[:28]
    suffix = latin or hashlib.sha256(theme.encode("utf-8")).hexdigest()[:10]
    return f"{timestamp}-{suffix}"


def create_plan(theme: str) -> dict:
    cleaned = " ".join(theme.split())
    if not cleaned:
        raise ValueError("테마를 한 문장 이상 입력해 주세요.")

    tracks = []
    for index, title in enumerate(TRACK_TITLES, start=1):
        prompt = (
            f"Instrumental jazz inspired by: {cleaned}. "
            "Warm acoustic piano, upright bass, soft brushed drums, subtle saxophone, "
            "slow relaxed tempo, cohesive late-night atmosphere, no vocals, "
            f"track {index} of a continuous album, gentle ending."
        )
        tracks.append(
            {
                "index": index,
                "title": title,
                "prompt": prompt,
                "status": "planned",
                "sourcePath": None,
                "durationSeconds": None,
                "chapterStartSeconds": None,
            }
        )

    return {
        "theme": cleaned,
        "direction": (
            f"'{cleaned}'의 정서를 중심으로 피아노, 콘트라베이스, 브러시 드럼이 "
            "자연스럽게 이어지는 느린 인스트루멘털 재즈 앨범을 제작한다."
        ),
        "imagePrompt": (
            f"Cinematic still image for a relaxing jazz album inspired by: {cleaned}. "
            "Elegant Seoul atmosphere, warm practical lighting, deep shadows, calm and "
            "timeless mood, photorealistic, tasteful composition, 16:9 landscape, "
            "no people looking at camera, no letters, no logo, no watermark."
        ),
        "tracks": tracks,
    }


def write_manual_guides(project_dir: Path, plan: dict) -> None:
    tracks_dir = project_dir / "work" / "tracks"
    image_dir = project_dir / "work" / "image"

    lines = [
        "SUNO MUSIC PLAN",
        f"Theme: {plan['theme']}",
        "",
        "Suno에서 각 프롬프트로 음악을 만든 뒤 아래 번호를 유지하여 저장하세요.",
        "예: 01_Opening_Glow.mp3, 02_Quiet_Window.mp3",
        "",
    ]
    for track in plan["tracks"]:
        lines.extend(
            [
                f"{track['index']:02d}. {track['title']}",
                track["prompt"],
                "",
            ]
        )

    (project_dir / "Suno_Prompts.txt").write_text("\n".join(lines), encoding="utf-8")
    (project_dir / "Image_Prompt.txt").write_text(
        "IMAGE PLAN\n"
        f"Theme: {plan['theme']}\n\n"
        f"{plan['imagePrompt']}\n\n"
        "생성한 가로 이미지를 work/image 폴더에 넣으세요.\n",
        encoding="utf-8",
    )
    (project_dir / "README_FIRST.txt").write_text(
        "1. Suno_Prompts.txt를 보고 Suno에서 음악을 만듭니다.\n"
        f"2. 음악 파일을 이 폴더에 넣습니다:\n{tracks_dir}\n\n"
        "3. Image_Prompt.txt를 보고 원하는 이미지 생성 서비스에서 이미지를 만듭니다.\n"
        f"4. 이미지 파일을 이 폴더에 넣습니다:\n{image_dir}\n\n"
        "5. 프로그램 화면으로 돌아와 '파일 확인 후 영상 만들기'를 누릅니다.\n",
        encoding="utf-8",
    )

