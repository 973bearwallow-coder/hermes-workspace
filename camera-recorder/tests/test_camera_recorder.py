import json
import os
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

import camera_recorder as recorder


class RecorderTests(unittest.TestCase):
    def test_load_config_rejects_unsafe_camera_name(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "config.json"
            path.write_text(json.dumps({
                "storage_root": str(Path(td) / "recordings"),
                "retention_hours": 24,
                "segment_seconds": 300,
                "min_free_gb": 1,
                "cameras": [{"name": "../escape", "url_env": "CAMERA_URL"}],
            }))
            with self.assertRaisesRegex(ValueError, "safe slug"):
                recorder.load_config(path)

    def test_cleanup_removes_expired_recordings_only_inside_root(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "recordings"
            camera = root / "camera_1"
            camera.mkdir(parents=True)
            old = camera / "old.mkv"
            fresh = camera / "fresh.mkv"
            outside = Path(td) / "outside.mkv"
            for path in (old, fresh, outside):
                path.write_bytes(b"video")
            stale = time.time() - 7200
            os.utime(old, (stale, stale))
            os.utime(outside, (stale, stale))

            removed = recorder.cleanup_recordings(root, retention_hours=1, min_free_gb=0)

            self.assertEqual(removed, [old])
            self.assertFalse(old.exists())
            self.assertTrue(fresh.exists())
            self.assertTrue(outside.exists())

    def test_record_local_media_creates_playable_private_segment(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            source = td / "source.mkv"
            subprocess.run([
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "testsrc=size=160x120:rate=5",
                "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(source),
            ], check=True)
            root = td / "recordings"
            segments = recorder.record_stream(
                source=str(source), camera_name="test_camera", storage_root=root,
                segment_seconds=1, stop_after_seconds=1.5,
            )
            self.assertGreaterEqual(len(segments), 1)
            for segment in segments:
                self.assertTrue(segment.resolve().is_relative_to(root.resolve()))
                self.assertEqual(segment.stat().st_mode & 0o777, 0o600)
                probe = subprocess.run([
                    "ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=codec_name", "-of", "csv=p=0", str(segment),
                ], capture_output=True, text=True)
                self.assertEqual(probe.returncode, 0, probe.stderr)
                self.assertIn("h264", probe.stdout)


if __name__ == "__main__":
    unittest.main()
