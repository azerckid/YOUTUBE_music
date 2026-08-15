from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from app.media import (
    ProductionError,
    analyze_tracks,
    ensure_disk_space,
    format_timestamp,
    resolve_font_path,
    write_concat_file,
    write_metadata,
)
from app.mood import MAX_IMAGE_BYTES, analyze_thumbnail, load_thumbnail
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
from tests.support import bright_thumbnail, dark_thumbnail, gradient_bytes


def sample_mood(data: bytes | None = None) -> dict:
    return analyze_thumbnail(data or dark_thumbnail())[2]


class MoodTests(unittest.TestCase):
    def test_dark_cool_cover_is_read_as_dark_and_cool(self) -> None:
        mood = sample_mood(dark_thumbnail())
        self.assertIn("깊은 어둠", mood["tags"])
        self.assertIn("차가운 색조", mood["tags"])
        self.assertLess(mood["brightness"], 0.22)
        self.assertLess(mood["warmth"], 0.35)
        self.assertIn("very slow tempo", mood["musicPhrase"])

    def test_bright_warm_cover_produces_a_different_direction(self) -> None:
        dark = sample_mood(dark_thumbnail())
        bright = sample_mood(bright_thumbnail())
        self.assertIn("밝고 열린 빛", bright["tags"])
        self.assertIn("따뜻한 색조", bright["tags"])
        self.assertGreater(bright["brightness"], dark["brightness"])
        self.assertGreater(bright["warmth"], dark["warmth"])
        self.assertNotEqual(bright["musicPhrase"], dark["musicPhrase"])

    def test_palette_and_summary_are_reported(self) -> None:
        mood = sample_mood()
        self.assertEqual(len(mood["tags"]), 4)
        self.assertEqual(mood["summary"], " · ".join(mood["tags"]))
        self.assertTrue(all(color.startswith("#") for color in mood["palette"]))

    def test_undersized_image_is_rejected(self) -> None:
        with self.assertRaises(ValueError) as captured:
            load_thumbnail(gradient_bytes(size=(320, 180)))
        self.assertIn("640", str(captured.exception))

    def test_non_image_payload_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_thumbnail(b"this is definitely not an image")

    def test_empty_and_oversized_payloads_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_thumbnail(b"")
        with self.assertRaises(ValueError):
            load_thumbnail(b"\x00" * (MAX_IMAGE_BYTES + 1))


class PlannerTests(unittest.TestCase):
    def test_plan_contains_eight_ordered_tracks(self) -> None:
        plan = create_plan("비 오는 서울의 밤", sample_mood())
        self.assertEqual(len(plan["tracks"]), 8)
        self.assertEqual([track["index"] for track in plan["tracks"]], list(range(1, 9)))
        self.assertEqual(
            [track["vocalMode"] for track in plan["tracks"]],
            ["vocal", "instrumental"] * 4,
        )
        self.assertTrue(
            all("Original lyrics" in track["prompt"] for track in plan["tracks"][::2])
        )
        self.assertTrue(
            all("no vocals" in track["prompt"] for track in plan["tracks"][1::2])
        )

    def test_every_prompt_carries_the_cover_mood(self) -> None:
        mood = sample_mood()
        plan = create_plan("비 오는 서울의 밤", mood)
        self.assertTrue(
            all(mood["musicPhrase"] in track["prompt"] for track in plan["tracks"])
        )
        self.assertIn(mood["summary"], plan["direction"])

    def test_cover_mood_changes_the_generated_prompts(self) -> None:
        dark = create_plan("같은 테마", sample_mood(dark_thumbnail()))
        bright = create_plan("같은 테마", sample_mood(bright_thumbnail()))
        self.assertNotEqual(
            dark["tracks"][0]["prompt"], bright["tracks"][0]["prompt"]
        )

    def test_blank_theme_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_plan("   ", sample_mood())

    def test_korean_theme_gets_safe_id(self) -> None:
        project_id = safe_project_id("서울의 밤", datetime(2026, 8, 11, 15, 30, 0))
        self.assertRegex(project_id, r"^20260811-153000-[a-f0-9]{10}$")

    def test_track_analysis_preserves_vocal_mode(self) -> None:
        manifest = create_plan("비 오는 서울의 밤", sample_mood())
        tracks = [Path(f"{index:02d}.mp3") for index in range(1, 9)]
        with patch("app.media.probe_duration", return_value=60.0):
            analyze_tracks(manifest, tracks, Path("unused.log"))
        self.assertEqual(
            [track["vocalMode"] for track in manifest["tracks"]],
            ["vocal", "instrumental"] * 4,
        )


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

    def test_metadata_describes_vocal_and_instrumental_jazz(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            write_metadata(
                output,
                "서울의 밤",
                [{"title": "Opening Glow", "start": 0.0}],
                180.0,
            )
            title = (output / "Title.txt").read_text(encoding="utf-8")
            description = (output / "Description.txt").read_text(encoding="utf-8")
            self.assertIn("Vocal & Instrumental Jazz", title)
            self.assertIn("보컬이 있는 곡과 연주곡", description)
            self.assertNotIn("SleepMusic", description)


class ProjectTests(unittest.TestCase):
    def test_project_creation_writes_manual_guides(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                manifest = create_project("새벽 서울 피아노 재즈", dark_thumbnail())
                root = Path(temp) / manifest["projectId"]
                self.assertEqual(manifest["status"], "waiting_for_files")
                self.assertTrue((root / "Suno_Prompts.txt").exists())
                guide = (root / "Suno_Prompts.txt").read_text(encoding="utf-8")
                self.assertIn("01. Opening Glow [가사·보컬]", guide)
                self.assertIn("02. Quiet Window [연주곡]", guide)
                self.assertIn(manifest["mood"]["summary"], guide)
                self.assertTrue((root / "Cover_Mood.txt").exists())
                self.assertFalse((root / "Image_Prompt.txt").exists())
                self.assertTrue((root / "work" / "tracks").is_dir())
                self.assertTrue((root / "work" / "image").is_dir())

    def test_registered_thumbnail_is_stored_and_analyzed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                manifest = create_project("썸네일 등록 테스트", dark_thumbnail())
                thumbnail = Path(manifest["thumbnail"])
                statuses = {step["id"]: step["status"] for step in manifest["steps"]}
                self.assertTrue(thumbnail.exists())
                self.assertEqual(thumbnail.name, "Thumbnail.jpg")
                self.assertEqual(thumbnail.read_bytes(), dark_thumbnail())
                self.assertEqual(statuses["image_analysis"], "completed")
                self.assertEqual(statuses["manual_assets"], "waiting")
                self.assertIn("깊은 어둠", manifest["mood"]["tags"])

    def test_project_is_not_created_when_thumbnail_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                with self.assertRaises(ValueError):
                    create_project("잘못된 이미지", b"not an image at all")
                self.assertEqual(list(Path(temp).iterdir()), [])

    def test_path_traversal_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            project_path("../outside")

    def test_begin_run_is_immediate_and_rejects_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                created = create_project("실행 상태 테스트", dark_thumbnail())
                running = begin_project_run(created["projectId"])
                self.assertEqual(running["status"], "running")
                with self.assertRaises(ProjectStateError):
                    begin_project_run(created["projectId"])

    def test_interrupted_run_is_recovered_without_losing_completed_steps(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with patch("app.project.PROJECTS_ROOT", Path(temp)):
                manifest = create_project("복구 테스트", dark_thumbnail())
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
