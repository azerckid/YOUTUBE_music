from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app.media import (
    ProductionError,
    ensure_disk_space,
    format_timestamp,
    resolve_font_path,
    write_concat_file,
)
from app.planner import create_plan, safe_project_id
from app.project import (
    ProjectStateError,
    begin_project_run,
    create_project,
    load_project,
    project_path,
    recover_interrupted_projects,
    save_project,
)
from app.server import host_is_allowed, origin_is_allowed


class PlannerTests(unittest.TestCase):
    def test_plan_contains_eight_ordered_tracks(self) -> None:
        plan = create_plan("비 오는 서울의 밤")
        self.assertEqual(len(plan["tracks"]), 8)
        self.assertEqual([track["index"] for track in plan["tracks"]], list(range(1, 9)))
        self.assertTrue(all("no vocals" in track["prompt"] for track in plan["tracks"]))

    def test_blank_theme_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_plan("   ")

    def test_korean_theme_gets_safe_id(self) -> None:
        project_id = safe_project_id("서울의 밤", datetime(2026, 8, 11, 15, 30, 0))
        self.assertRegex(project_id, r"^20260811-153000-[a-f0-9]{10}$")


class MediaTests(unittest.TestCase):
    def test_timestamp_formats_long_video(self) -> None:
        self.assertEqual(format_timestamp(0), "00:00")
        self.assertEqual(format_timestamp(3661), "01:01:01")

    def test_concat_repeats_whole_set_three_times(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            tracks = [root / "01.m4a", root / "02.m4a"]
            output = root / "playlist.txt"
            write_concat_file(tracks, output, 3)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 6)
            self.assertIn("01.m4a", lines[0])
            self.assertIn("02.m4a", lines[1])
            self.assertIn("01.m4a", lines[2])


class ProjectTests(unittest.TestCase):
    def test_project_creation_writes_manual_guides(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                manifest = create_project("새벽 서울 피아노 재즈")
                root = Path(temp) / manifest["projectId"]
                self.assertEqual(manifest["status"], "waiting_for_files")
                self.assertTrue((root / "Suno_Prompts.txt").exists())
                self.assertTrue((root / "Image_Prompt.txt").exists())
                self.assertTrue((root / "work" / "tracks").is_dir())
                self.assertTrue((root / "work" / "image").is_dir())

    def test_path_traversal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            project_path("../outside")

    def test_begin_run_is_immediate_and_rejects_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                created = create_project("실행 상태 테스트")
                running = begin_project_run(created["projectId"])
                self.assertEqual(running["status"], "running")
                with self.assertRaises(ProjectStateError):
                    begin_project_run(created["projectId"])

    def test_interrupted_run_is_recovered_without_losing_completed_steps(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                manifest = create_project("복구 테스트")
                manifest["status"] = "running"
                manifest["currentStep"] = "video_render"
                for step in manifest["steps"]:
                    if step["id"] == "cover":
                        step["status"] = "completed"
                    if step["id"] == "video_render":
                        step["status"] = "running"
                save_project(manifest)

                self.assertEqual(recover_interrupted_projects(), 1)
                recovered = load_project(manifest["projectId"])
                statuses = {step["id"]: step["status"] for step in recovered["steps"]}
                self.assertEqual(recovered["status"], "failed")
                self.assertEqual(statuses["cover"], "completed")
                self.assertEqual(statuses["video_render"], "failed")
                self.assertTrue(recovered["error"]["retryable"])


class GuardTests(unittest.TestCase):
    def test_local_host_and_origin_are_allowed(self) -> None:
        self.assertTrue(host_is_allowed("127.0.0.1:8765", 8765))
        self.assertTrue(host_is_allowed("localhost:8765", 8765))
        self.assertTrue(origin_is_allowed("http://127.0.0.1:8765", 8765))
        self.assertTrue(origin_is_allowed(None, 8765))

    def test_remote_host_and_origin_are_rejected(self) -> None:
        self.assertFalse(host_is_allowed("example.com:8765", 8765))
        self.assertFalse(host_is_allowed("127.0.0.1:9999", 8765))
        self.assertFalse(origin_is_allowed("https://example.com", 8765))

    def test_missing_font_has_actionable_error(self) -> None:
        with patch("app.media.FONT_CANDIDATES", (Path("/missing/font.ttf"),)):
            with self.assertRaises(ProductionError) as captured:
                resolve_font_path()
        self.assertIn("글꼴", str(captured.exception))
        self.assertTrue(captured.exception.retryable)

    def test_disk_space_guard_rejects_low_space(self) -> None:
        with patch(
            "app.media.shutil.disk_usage",
            return_value=SimpleNamespace(free=100_000_000),
        ):
            with self.assertRaises(ProductionError):
                ensure_disk_space(Path("."), 3600)


if __name__ == "__main__":
    unittest.main()
