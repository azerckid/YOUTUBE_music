from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from app.media import (
    ProductionError,
    create_cover,
    normalize_tracks,
    probe_duration,
    render_video,
    validate_video,
    produce_project,
)
from app.project import begin_project_run, create_project, load_project, save_project


class MediaIntegrationTests(unittest.TestCase):
    def test_short_video_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "production.log"
            source_image = root / "source.jpg"
            Image.new("RGB", (1280, 720), (31, 42, 58)).save(source_image)
            cover = root / "Cover.jpg"
            create_cover(source_image, cover, "비 오는 서울의 밤")

            tracks = []
            for index, frequency in enumerate((330, 440), start=1):
                track = root / f"{index:02d}.wav"
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        f"sine=frequency={frequency}:duration=1",
                        "-c:a", "pcm_s16le", str(track),
                    ],
                    check=True,
                    capture_output=True,
                )
                tracks.append(track)

            normalized = normalize_tracks(tracks, root / "audio", log)
            output = root / "YouTube_Final.mp4"
            render_video(cover, normalized, 3, output, root / "audio", log)
            expected = sum(probe_duration(track, log) for track in tracks) * 3
            validation = validate_video(output, expected, log)

            self.assertTrue(output.exists())
            self.assertTrue(validation["passed"], validation)

    def test_failed_metadata_resume_reuses_completed_video(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            projects_root = Path(temp) / "projects"
            with patch("app.project.PROJECTS_ROOT", projects_root):
                manifest = create_project("재시작 테스트")
                root = projects_root / manifest["projectId"]
                source_image = root / "work" / "image" / "cover.jpg"
                Image.new("RGB", (1280, 720), (36, 43, 54)).save(source_image)
                track = root / "work" / "tracks" / "01_track.wav"
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        "sine=frequency=390:duration=1",
                        "-c:a", "pcm_s16le", str(track),
                    ],
                    check=True,
                    capture_output=True,
                )

                begin_project_run(manifest["projectId"])
                produce_project(manifest["projectId"])
                completed = load_project(manifest["projectId"])
                self.assertEqual(completed["status"], "completed")
                video = root / "output" / "YouTube_Final.mp4"
                video_mtime = video.stat().st_mtime_ns

                completed["status"] = "failed"
                completed["currentStep"] = "metadata"
                for step in completed["steps"]:
                    if step["id"] == "metadata":
                        step["status"] = "failed"
                    if step["id"] == "output_ready":
                        step["status"] = "pending"
                (root / "output" / "Title.txt").unlink()
                save_project(completed)

                begin_project_run(manifest["projectId"])
                produce_project(manifest["projectId"])
                resumed = load_project(manifest["projectId"])
                self.assertEqual(resumed["status"], "completed")
                self.assertEqual(video.stat().st_mtime_ns, video_mtime)
                self.assertTrue((root / "output" / "Title.txt").exists())

    def test_changed_older_track_does_not_reuse_stale_audio(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            projects_root = Path(temp) / "projects"
            with patch("app.project.PROJECTS_ROOT", projects_root):
                manifest = create_project("오디오 교체 테스트")
                root = projects_root / manifest["projectId"]
                Image.new("RGB", (1280, 720), (36, 43, 54)).save(
                    root / "work" / "image" / "cover.jpg"
                )
                track = root / "work" / "tracks" / "01_track.wav"
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        "sine=frequency=330:duration=1", "-c:a", "pcm_s16le", str(track),
                    ],
                    check=True,
                    capture_output=True,
                )

                begin_project_run(manifest["projectId"])
                with patch(
                    "app.media.write_metadata",
                    side_effect=ProductionError("메타데이터 테스트 실패"),
                ):
                    produce_project(manifest["projectId"])
                normalized = root / "work" / "audio" / "01.m4a"
                old_digest = hashlib.sha256(normalized.read_bytes()).hexdigest()

                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "lavfi", "-i",
                        "sine=frequency=660:duration=1", "-c:a", "pcm_s16le", str(track),
                    ],
                    check=True,
                    capture_output=True,
                )
                os.utime(track, (1, 1))

                begin_project_run(manifest["projectId"])
                produce_project(manifest["projectId"])
                new_digest = hashlib.sha256(normalized.read_bytes()).hexdigest()

                self.assertNotEqual(new_digest, old_digest)
                self.assertEqual(load_project(manifest["projectId"])["status"], "completed")


if __name__ == "__main__":
    unittest.main()
