#!/usr/bin/env python3
"""Local, privacy-first dog detector for authenticated RTSP cameras."""
from __future__ import annotations

import argparse
import ipaddress
import json
import math
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

CAMERA_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
ENV_RE = re.compile(r"^[A-Z_][A-Z0-9_]*$")


class ConfigError(ValueError):
    pass


def _finite_number(value: Any, name: str, minimum: float, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ConfigError(f"{name} must be a number")
    value = float(value)
    if not math.isfinite(value) or value < minimum or (maximum is not None and value > maximum):
        raise ConfigError(f"{name} is out of range")
    return value


def _strict_positive_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ConfigError(f"{name} must be a positive integer")
    return value


def _validate_slug(name: Any) -> str:
    if not isinstance(name, str) or not CAMERA_RE.fullmatch(name):
        raise ConfigError("invalid camera name")
    return name


def load_config(path: str | Path) -> dict[str, Any]:
    try:
        cfg = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load configuration: {exc}") from exc
    if not isinstance(cfg, dict) or not isinstance(cfg.get("cameras"), list) or not cfg["cameras"]:
        raise ConfigError("cameras must be a non-empty list")
    cfg["retention_days"] = _strict_positive_int(cfg.get("retention_days"), "retention_days")
    cfg["max_events_per_camera"] = _strict_positive_int(cfg.get("max_events_per_camera"), "max_events_per_camera")
    if not isinstance(cfg.get("model_path"), str) or not cfg["model_path"]:
        raise ConfigError("model_path is required")
    if not isinstance(cfg.get("storage_root"), str) or not cfg["storage_root"]:
        raise ConfigError("storage_root is required")
    seen: set[str] = set()
    for camera in cfg["cameras"]:
        if not isinstance(camera, dict):
            raise ConfigError("camera entries must be objects")
        name = _validate_slug(camera.get("name"))
        if name in seen:
            raise ConfigError("duplicate camera name")
        seen.add(name)
        if not isinstance(camera.get("location"), str) or not camera["location"].strip():
            raise ConfigError("camera location is required")
        if not isinstance(camera.get("url_env"), str) or not ENV_RE.fullmatch(camera["url_env"]):
            raise ConfigError("invalid url_env")
        camera["sample_every_seconds"] = _finite_number(camera.get("sample_every_seconds"), "sample_every_seconds", 0.000001)
        camera["min_confidence"] = _finite_number(camera.get("min_confidence"), "min_confidence", 0.0, 1.0)
        camera["consecutive_frames"] = _strict_positive_int(camera.get("consecutive_frames"), "consecutive_frames")
        camera["cooldown_seconds"] = _finite_number(camera.get("cooldown_seconds"), "cooldown_seconds", 0.0)
        for key in ("mapping_verified", "alerts_enabled"):
            if type(camera.get(key)) is not bool:
                raise ConfigError(f"{key} must be a boolean")
        if camera["alerts_enabled"]:
            raise ConfigError("alerts are unavailable until notifier acceptance is complete")
    return cfg


def _contained(root: Path, candidate: Path) -> None:
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ConfigError("event path escapes storage root") from exc


def _private_write(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(data)


def save_event(storage_root: str | Path, camera_name: str, jpeg: bytes, confidence: float) -> Path:
    name = _validate_slug(camera_name)
    confidence = _finite_number(confidence, "confidence", 0.0, 1.0)
    root = Path(storage_root).resolve()
    camera_dir = root / name
    _contained(root, camera_dir)
    camera_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(camera_dir, 0o700)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    stem = camera_dir / f"dog-{stamp}"
    image_path = stem.with_suffix(".jpg")
    metadata_path = stem.with_suffix(".json")
    _contained(root, image_path)
    _contained(root, metadata_path)
    metadata = {
        "camera": name,
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "object": "dog",
        "confidence": round(confidence, 4),
        "dog_identity": "unknown",
        "continuous_video_recorded": False,
        "alert_sent": False,
    }
    _private_write(image_path, jpeg)
    _private_write(metadata_path, (json.dumps(metadata, sort_keys=True) + "\n").encode())
    return metadata_path


def _write_health(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    temp = path.with_suffix(".tmp")
    fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as handle:
        json.dump(payload, handle, sort_keys=True)
        handle.write("\n")
    os.replace(temp, path)


def prune_events(storage_root: Path, name: str, retention_days: int, maximum: int) -> None:
    directory = storage_root / _validate_slug(name)
    if not directory.exists():
        return
    cutoff = time.time() - retention_days * 86400
    metadata = sorted(directory.glob("dog-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for index, item in enumerate(metadata):
        if item.stat().st_mtime < cutoff or index >= maximum:
            image = item.with_suffix(".jpg")
            item.unlink(missing_ok=True)
            image.unlink(missing_ok=True)


def sync_camera_clock(stream_url: str, now: str | None = None, session: Any = None) -> bool:
    """Sync a private LAN camera to the host wall clock without exposing credentials."""
    from requests import Session
    from requests.auth import HTTPDigestAuth

    parsed = urlsplit(stream_url)
    if parsed.scheme != "rtsp" or not parsed.hostname or parsed.username is None or parsed.password is None:
        raise ConfigError("clock sync requires an authenticated RTSP URL")
    try:
        if not ipaddress.ip_address(parsed.hostname).is_private:
            raise ConfigError("clock sync is restricted to private IP addresses")
    except ValueError as exc:
        raise ConfigError("clock sync requires a private IP address") from exc
    client = session or Session()
    auth = HTTPDigestAuth(unquote(parsed.username), unquote(parsed.password))
    base = f"http://{parsed.hostname}"
    disable_ntp = client.get(
        base + "/cgi-bin/configManager.cgi",
        params={"action": "setConfig", "NTP.Enable": "false"},
        auth=auth,
        timeout=8,
    )
    wall_clock = now or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    set_time = client.get(
        base + "/cgi-bin/global.cgi",
        params={"action": "setCurrentTime", "time": wall_clock},
        auth=auth,
        timeout=8,
    )
    return disable_ntp.status_code == 200 and set_time.status_code == 200


def run_camera(cfg: dict[str, Any], camera: dict[str, Any], once: bool = False) -> int:
    import cv2
    from ultralytics import YOLO

    stream_url = os.environ.get(camera["url_env"])
    if not stream_url:
        raise ConfigError(f"missing required secret environment variable: {camera['url_env']}")
    model = YOLO(cfg["model_path"])
    dog_class_ids = [key for key, value in model.names.items() if str(value).lower() == "dog"]
    if not dog_class_ids:
        raise RuntimeError("model has no dog class")
    health_path = Path(cfg["health_path"])
    storage_root = Path(cfg["storage_root"])
    failures = 0
    consecutive = 0
    last_event = 0.0
    last_clock_sync = 0.0
    if not sync_camera_clock(stream_url):
        raise RuntimeError("camera clock sync failed")
    last_clock_sync = time.time()
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                failures += 1
                cap.release()
                if failures >= 5:
                    _write_health(health_path, {"status": "failed_closed", "camera": camera["name"], "read_failures": failures})
                    return 2
                _write_health(health_path, {"status": "reconnecting", "camera": camera["name"], "read_failures": failures})
                time.sleep(1)
                cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
                continue
            failures = 0
            if time.time() - last_clock_sync >= 3600:
                if sync_camera_clock(stream_url):
                    last_clock_sync = time.time()
            detections = model.predict(frame, classes=dog_class_ids, conf=camera["min_confidence"], verbose=False)[0]
            boxes = detections.boxes
            dog_count = 0 if boxes is None else len(boxes)
            best_confidence = 0.0
            event_saved = False
            if dog_count:
                consecutive += 1
                best = max(boxes, key=lambda box: float(box.conf[0]))
                best_confidence = float(best.conf[0])
                if consecutive >= camera["consecutive_frames"] and time.time() - last_event >= camera["cooldown_seconds"]:
                    x1, y1, x2, y2 = (int(x) for x in best.xyxy[0].tolist())
                    height, width = frame.shape[:2]
                    pad_x, pad_y = int((x2 - x1) * 0.15), int((y2 - y1) * 0.15)
                    crop = frame[max(0, y1-pad_y):min(height, y2+pad_y), max(0, x1-pad_x):min(width, x2+pad_x)]
                    encoded, buffer = cv2.imencode(".jpg", crop)
                    if encoded:
                        save_event(storage_root, camera["name"], buffer.tobytes(), best_confidence)
                        prune_events(storage_root, camera["name"], cfg["retention_days"], cfg["max_events_per_camera"])
                        last_event = time.time()
                        event_saved = True
            else:
                consecutive = 0
            _write_health(health_path, {
                "status": "ok",
                "camera": camera["name"],
                "location": camera["location"],
                "frame_received": True,
                "dog_count": dog_count,
                "best_confidence": round(best_confidence, 4),
                "event_saved": event_saved,
                "alerts_enabled": False,
                "mapping_verified": camera["mapping_verified"],
                "checked_at": datetime.now(timezone.utc).isoformat(),
            })
            if once:
                return 0
            time.sleep(camera["sample_every_seconds"])
    finally:
        cap.release()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--camera", default="living_room")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    cfg = load_config(args.config)
    matches = [c for c in cfg["cameras"] if c["name"] == args.camera]
    if not matches:
        raise ConfigError("requested camera is not configured")
    return run_camera(cfg, matches[0], once=args.once)


if __name__ == "__main__":
    raise SystemExit(main())
