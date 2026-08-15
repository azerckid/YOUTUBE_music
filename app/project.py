from __future__ import annotations

import json
import os
import tempfile
import threading
from datetime import datetime
from pathlib import Path

from .mood import analyze_thumbnail
from .planner import clean_theme, create_plan, safe_project_id, write_manual_guides


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_ROOT = ROOT / "projects"
MANIFEST_LOCK = threading.Lock()
RUNNABLE_STATUSES = {"waiting_for_files", "failed"}


class ProjectStateError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_LOCK:
        descriptor, temp_name = tempfile.mkstemp(
            prefix=f".{path.name}.", dir=path.parent, text=True
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(data, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
        except Exception:
            Path(temp_name).unlink(missing_ok=True)
            raise


def project_path(project_id: str) -> Path:
    if not project_id or project_id != Path(project_id).name:
        raise ValueError("유효하지 않은 프로젝트 ID입니다.")
    path = (PROJECTS_ROOT / project_id).resolve()
    if path.parent != PROJECTS_ROOT.resolve():
        raise ValueError("프로젝트 경로가 허용 범위를 벗어났습니다.")
    return path


def load_project(project_id: str) -> dict:
    path = project_path(project_id) / "project.json"
    if not path.exists():
        raise FileNotFoundError("프로젝트를 찾을 수 없습니다.")
    return json.loads(path.read_text(encoding="utf-8"))


def save_project(manifest: dict) -> None:
    manifest["updatedAt"] = now_iso()
    atomic_write_json(project_path(manifest["projectId"]) / "project.json", manifest)


def create_project(theme: str, thumbnail_bytes: bytes) -> dict:
    cleaned_theme = clean_theme(theme)
    image, suffix, mood = analyze_thumbnail(thumbnail_bytes)
    image.close()
    plan = create_plan(cleaned_theme, mood)
    base_project_id = safe_project_id(plan["theme"])
    project_id = base_project_id
    counter = 2
    PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)
    while True:
        directory = project_path(project_id)
        try:
            directory.mkdir()
            break
        except FileExistsError:
            project_id = f"{base_project_id}-{counter}"
            counter += 1

    for relative in ("work/tracks", "work/image", "work/audio", "logs", "output"):
        (directory / relative).mkdir(parents=True)

    thumbnail_path = directory / "work" / "image" / f"Thumbnail{suffix}"
    thumbnail_path.write_bytes(thumbnail_bytes)

    steps = [
        {"id": "theme_plan", "label": "테마 분석과 제작 방향", "status": "completed"},
        {"id": "image_analysis", "label": "썸네일 분위기 분석", "status": "completed"},
        {"id": "music_plan", "label": "Suno 음악 제작 계획", "status": "completed"},
        {"id": "manual_assets", "label": "Suno 음악 준비", "status": "waiting"},
        {"id": "cover", "label": "영상용 이미지 완성", "status": "pending"},
        {"id": "audio_analysis", "label": "음악 분석과 챕터 계산", "status": "pending"},
        {"id": "audio_assembly", "label": "음악 연결과 3회 반복", "status": "pending"},
        {"id": "video_render", "label": "최종 영상 생성", "status": "pending"},
        {"id": "metadata", "label": "업로드 문구 생성", "status": "pending"},
        {"id": "quality_check", "label": "완성 영상 자동검사", "status": "pending"},
        {"id": "output_ready", "label": "결과물 정리", "status": "pending"},
    ]
    manifest = {
        "schemaVersion": 1,
        "mode": "manual-assets",
        "projectId": project_id,
        "theme": plan["theme"],
        "status": "waiting_for_files",
        "currentStep": "manual_assets",
        "repeatCount": 3,
        "direction": plan["direction"],
        "mood": plan["mood"],
        "thumbnail": str(thumbnail_path),
        "tracks": plan["tracks"],
        "steps": steps,
        "progress": 20,
        "message": "썸네일 분위기에 맞춘 Suno 프롬프트를 만들었습니다. 음악을 준비해 지정 폴더에 넣어 주세요.",
        "output": None,
        "validation": None,
        "assetSignature": None,
        "error": None,
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
    write_manual_guides(directory, plan, thumbnail_path)
    save_project(manifest)
    return manifest


def begin_project_run(project_id: str) -> dict:
    manifest = load_project(project_id)
    if manifest.get("status") not in RUNNABLE_STATUSES:
        if manifest.get("status") == "running":
            raise ProjectStateError("이미 제작이 진행 중입니다.")
        if manifest.get("status") == "completed":
            raise ProjectStateError("이미 완료된 프로젝트입니다. 새 테마로 프로젝트를 만들어 주세요.")
        raise ProjectStateError("현재 상태에서는 제작을 시작할 수 없습니다.")

    for step in manifest["steps"]:
        if step["status"] in {"running", "failed"}:
            step["status"] = "pending"
    manifest["status"] = "running"
    manifest["error"] = None
    manifest["message"] = "준비된 파일을 확인하고 제작을 시작합니다."
    manifest["runStartedAt"] = now_iso()
    save_project(manifest)
    return manifest


def update_step(
    manifest: dict,
    step_id: str,
    status: str,
    message: str,
    progress: int | None = None,
) -> None:
    for step in manifest["steps"]:
        if step["id"] == step_id:
            step["status"] = status
            break
    manifest["currentStep"] = step_id
    manifest["message"] = message
    if progress is not None:
        manifest["progress"] = progress
    save_project(manifest)


def latest_project() -> dict | None:
    if not PROJECTS_ROOT.exists():
        return None
    manifests = sorted(
        PROJECTS_ROOT.glob("*/project.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    if not manifests:
        return None
    return json.loads(manifests[0].read_text(encoding="utf-8"))


def recover_interrupted_projects() -> int:
    if not PROJECTS_ROOT.exists():
        return 0
    recovered = 0
    for path in PROJECTS_ROOT.glob("*/project.json"):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if manifest.get("status") != "running":
            continue
        current_step = manifest.get("currentStep", "unknown")
        for step in manifest.get("steps", []):
            if step.get("id") == current_step and step.get("status") == "running":
                step["status"] = "failed"
        manifest["status"] = "failed"
        manifest["error"] = {
            "step": current_step,
            "message": "이전 실행이 정상적으로 종료되지 않았습니다.",
            "retryable": True,
            "action": "실패 단계부터 다시 시도해 주세요.",
        }
        manifest["message"] = manifest["error"]["message"]
        save_project(manifest)
        recovered += 1
    return recovered
