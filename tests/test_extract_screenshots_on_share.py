import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "scripts" / "extract_screenshots_on_share.py"
spec = importlib.util.spec_from_file_location("visual_review", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class VisualReviewTests(unittest.TestCase):
    def test_moments_are_evidence_bearing_and_deduplicated(self):
        payload = {"segments": [
            {"start": 10, "text": "Let me share my screen."},
            {"start": 20, "text": "Look at this dashboard."},
            {"start": 55, "text": "I will pull up the final page."},
            {"start": 90, "text": "Nothing visual here."},
        ]}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "transcript.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            moments = mod.find_visual_moments(path)
        self.assertEqual([10.0, 55.0], [m["timestamp_seconds"] for m in moments])
        self.assertIn("dashboard", moments[0]["transcript_evidence"].lower())
        self.assertTrue(moments[0]["keywords"])

    @patch.object(mod, "video_duration", return_value=12.0)
    @patch.object(mod.subprocess, "run")
    def test_frames_cluster_and_clamp_to_video(self, run, _duration):
        with tempfile.TemporaryDirectory() as td:
            video = Path(td) / "call.mp4"
            video.write_bytes(b"synthetic")
            frames, duration = mod.extract_frames(
                video, [{"timestamp_seconds": 10.0}], Path(td) / "frames")
        self.assertEqual(12.0, duration)
        self.assertEqual([7.0, 10.0, 11.95], [f["timestamp_seconds"] for f in frames])
        self.assertEqual(3, run.call_count)

    @patch.object(mod, "video_duration", return_value=12.0)
    def test_empty_review_still_writes_manifest(self, _duration):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            video = root / "call.mp4"
            video.write_bytes(b"synthetic")
            transcript = root / "transcript.json"
            transcript.write_text('{"segments": []}', encoding="utf-8")
            out = root / "out"
            manifest = mod.run_review(video, transcript, out)
            persisted = json.loads((out / "review_manifest.json").read_text())
        self.assertEqual([], manifest["frames"])
        self.assertIn("does not validate", persisted["review_warning"])


if __name__ == "__main__":
    unittest.main()
