import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

from camera_dog_monitor import ConfigError, load_config, save_event, sync_camera_clock


BASE_CAMERA = {
    "name": "living_room",
    "location": "Living Room",
    "url_env": "LIVING_ROOM_RTSP_URL",
    "sample_every_seconds": 1.0,
    "min_confidence": 0.45,
    "consecutive_frames": 2,
    "cooldown_seconds": 30.0,
    "mapping_verified": True,
    "alerts_enabled": False,
}


def write_config(root, cameras):
    path = Path(root) / "config.json"
    path.write_text(json.dumps({
        "model_path": "/home/tom/yolov8n.pt",
        "storage_root": str(Path(root) / "events"),
        "retention_days": 7,
        "max_events_per_camera": 100,
        "cameras": cameras,
    }))
    return path


class ConfigTests(unittest.TestCase):
    def test_valid_config_loads(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = load_config(write_config(d, [BASE_CAMERA]))
            self.assertEqual(cfg["cameras"][0]["name"], "living_room")

    def test_duplicate_camera_names_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ConfigError):
                load_config(write_config(d, [BASE_CAMERA, BASE_CAMERA]))

    def test_path_traversal_and_bad_env_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for patch in ({"name": "../../outside"}, {"url_env": "bad-name"}):
                camera = dict(BASE_CAMERA, **patch)
                with self.assertRaises(ConfigError):
                    load_config(write_config(d, [camera]))

    def test_bad_numbers_and_booleans_rejected(self):
        fields = {
            "sample_every_seconds": [0, -1, True, float("nan")],
            "min_confidence": [-0.1, 1.1, True, float("inf")],
            "consecutive_frames": [0, -1, True, 1.5],
            "cooldown_seconds": [-1, True, float("nan")],
        }
        with tempfile.TemporaryDirectory() as d:
            for field, values in fields.items():
                for value in values:
                    with self.subTest(field=field, value=value):
                        camera = dict(BASE_CAMERA, **{field: value})
                        with self.assertRaises(ConfigError):
                            load_config(write_config(d, [camera]))

    def test_alerts_rejected_until_notifier_exists(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ConfigError):
                load_config(write_config(d, [dict(BASE_CAMERA, alerts_enabled=True)]))


class EventTests(unittest.TestCase):
    def test_event_is_private_and_minimal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "events"
            metadata = save_event(root, "living_room", b"jpeg", 0.91)
            crop = metadata.with_suffix(".jpg")
            doc = json.loads(metadata.read_text())
            self.assertEqual(stat.S_IMODE(metadata.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(crop.stat().st_mode), 0o600)
            self.assertEqual(doc["dog_identity"], "unknown")
            self.assertFalse(doc["continuous_video_recorded"])
            self.assertFalse(doc["alert_sent"])

    def test_sink_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "events"
            with self.assertRaises(ConfigError):
                save_event(root, "../escape", b"jpeg", 0.9)


class ClockSyncTests(unittest.TestCase):
    class Response:
        status_code = 200

    class Session:
        def __init__(self):
            self.calls = []

        def get(self, url, **kwargs):
            self.calls.append((url, kwargs))
            return ClockSyncTests.Response()

    def test_sync_uses_private_host_and_never_places_credentials_in_url(self):
        session = self.Session()
        self.assertTrue(sync_camera_clock(
            "rtsp://camera-user:camera-pass@192.168.1.25:554/live",
            now="2026-09-04 22:30:00",
            session=session,
        ))
        self.assertEqual(len(session.calls), 2)
        for url, _kwargs in session.calls:
            self.assertNotIn("camera-user", url)
            self.assertNotIn("camera-pass", url)
        self.assertEqual(session.calls[0][1]["params"]["NTP.Enable"], "false")
        self.assertEqual(session.calls[1][1]["params"]["time"], "2026-09-04 22:30:00")

    def test_sync_rejects_non_private_or_credentialless_urls(self):
        for value in ("http://192.168.1.25/live", "rtsp://192.168.1.25/live", "rtsp://u:p@8.8.8.8/live"):
            with self.subTest(value=value), self.assertRaises(ConfigError):
                sync_camera_clock(value, now="2026-09-04 22:30:00", session=self.Session())


if __name__ == "__main__":
    unittest.main()
