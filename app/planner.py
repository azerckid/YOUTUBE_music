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


def clean_theme(theme: str) -> str:
    cleaned = " ".join(theme.split())
    if not cleaned:
        raise ValueError("테마를 한 문장 이상 입력해 주세요.")
    return cleaned


def safe_project_id(theme: str, now: datetime | None = None) -> str:
    timestamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    latin = re.sub(r"[^a-z0-9]+", "-", theme.lower()).strip("-")[:28]
    suffix = latin or hashlib.sha256(theme.encode("utf-8")).hexdigest()[:10]
    return f"{timestamp}-{suffix}"


def create_plan(theme: str, mood: dict) -> dict:
    cleaned = clean_theme(theme)
    mood_phrase = mood["musicPhrase"]

    tracks = []
    for index, title in enumerate(TRACK_TITLES, start=1):
        vocal_mode = "vocal" if index % 2 == 1 else "instrumental"
        if vocal_mode == "vocal":
            prompt = (
                f"Vocal jazz song inspired by: {cleaned}. "
                f"Mood taken from the cover artwork: {mood_phrase}. "
                "Original lyrics that reflect the theme, warm intimate lead vocal, "
                "acoustic piano, upright bass, soft brushed drums, subtle saxophone, "
                "cohesive atmosphere, "
                f"track {index} of a continuous album, gentle ending."
            )
        else:
            prompt = (
                f"Instrumental jazz inspired by: {cleaned}. "
                f"Mood taken from the cover artwork: {mood_phrase}. "
                "Warm acoustic piano, upright bass, soft brushed drums, subtle saxophone, "
                "cohesive atmosphere, no vocals, "
                f"track {index} of a continuous album, gentle ending."
            )
        tracks.append(
            {
                "index": index,
                "title": title,
                "vocalMode": vocal_mode,
                "prompt": prompt,
                "status": "planned",
                "sourcePath": None,
                "durationSeconds": None,
                "chapterStartSeconds": None,
            }
        )

    return {
        "theme": cleaned,
        "mood": mood,
        "direction": (
            f"'{cleaned}'의 정서와 썸네일에서 읽은 분위기({mood['summary']})를 중심으로 "
            "피아노, 콘트라베이스, 브러시 드럼이 자연스럽게 이어지며 "
            "보컬곡과 연주곡이 번갈아 나오는 재즈 앨범을 제작한다."
        ),
        "tracks": tracks,
    }


def write_manual_guides(project_dir: Path, plan: dict, thumbnail_path: Path) -> None:
    tracks_dir = project_dir / "work" / "tracks"
    mood = plan["mood"]

    lines = [
        "SUNO MUSIC PLAN",
        f"Theme: {plan['theme']}",
        f"Cover mood: {mood['summary']}",
        f"Mood prompt: {mood['musicPhrase']}",
        "",
        "Suno에서 각 프롬프트로 음악을 만든 뒤 아래 번호를 유지하여 저장하세요.",
        "예: 01_Opening_Glow.mp3, 02_Quiet_Window.mp3",
        "",
    ]
    for track in plan["tracks"]:
        mode_label = "가사·보컬" if track["vocalMode"] == "vocal" else "연주곡"
        lines.extend(
            [
                f"{track['index']:02d}. {track['title']} [{mode_label}]",
                track["prompt"],
                "",
            ]
        )

    (project_dir / "Suno_Prompts.txt").write_text("\n".join(lines), encoding="utf-8")
    (project_dir / "Cover_Mood.txt").write_text(
        "COVER MOOD ANALYSIS\n"
        f"Theme: {plan['theme']}\n"
        f"Thumbnail: {thumbnail_path}\n\n"
        f"분위기 요약: {mood['summary']}\n"
        f"화면 인상: {mood['visualPhrase']}\n"
        f"음악 지시: {mood['musicPhrase']}\n\n"
        f"밝기 {mood['brightness']:.2f} · 채도 {mood['saturation']:.2f} · "
        f"대비 {mood['contrast']:.2f} · 따뜻함 {mood['warmth']:.2f}\n"
        f"주요 색상: {', '.join(mood['palette'])}\n",
        encoding="utf-8",
    )
    (project_dir / "README_FIRST.txt").write_text(
        "1. 등록한 썸네일 이미지의 분위기를 분석해 Suno_Prompts.txt를 만들었습니다.\n"
        "   분석 결과는 Cover_Mood.txt에서 확인할 수 있습니다.\n\n"
        "2. Suno_Prompts.txt를 보고 Suno에서 음악을 만듭니다.\n"
        f"3. 음악 파일을 이 폴더에 넣습니다:\n{tracks_dir}\n\n"
        "4. 프로그램 화면으로 돌아와 '파일 확인 후 영상 만들기'를 누릅니다.\n\n"
        f"등록한 썸네일 이미지는 여기에 저장되어 있습니다:\n{thumbnail_path}\n",
        encoding="utf-8",
    )
