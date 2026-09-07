#!/usr/bin/python3
"""Local, bounded RTSP recorder using PyAV without credentials in argv."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shutil
import signal
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import av

SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
_STOP = False


@dataclass(frozen=True)
class Camera:
    name: str
    url_env: str


@dataclass(frozen=True)
class Config:
    storage_root: Path
    health_root: Path
    retention_hours: float
    segment_seconds: int
    min_free_gb: float
    cameras: tuple[Camera, ...]


def _positive_number(value: Any, field: str, *, allow_zero: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    if value < 0 or (not allow_zero and value == 0):
        raise ValueError(f"{field} is out of range")
    return float(value)


def load_config(path: Path) -> Config:
    raw = json.loads(path.read_text())
    root = Path(raw["storage_root"]).expanduser().resolve()
    health = Path(raw.get("health_root", root.parent / "health")).expanduser().resolve()
    retention = _positive_number(raw["retention_hours"], "retention_hours")
    segment = _positive_number(raw["segment_seconds"], "segment_seconds")
    if not segment.is_integer():
        raise ValueError("segment_seconds must be an integer")
    min_free = _positive_number(raw.get("min_free_gb", 0), "min_free_gb", allow_zero=True)
    cameras: list[Camera] = []
    names: set[str] = set()
    for item in raw.get("cameras", []):
        name = item.get("name")
        env_name = item.get("url_env")
        if not isinstance(name, str) or SAFE_NAME.fullmatch(name) is None:
            raise ValueError("camera name must be a safe slug")
        if name in names:
            raise ValueError("camera names must be unique")
        if not isinstance(env_name, str) or ENV_NAME.fullmatch(env_name) is None:
            raise ValueError("url_env must be a safe environment-variable name")
        names.add(name)
        cameras.append(Camera(name, env_name))
    if not cameras:
        raise ValueError("at least one camera is required")
    return Config(root, health, retention, int(segment), min_free, tuple(cameras))


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(0o700)


def cleanup_recordings(storage_root: Path, retention_hours: float, min_free_gb: float) -> list[Path]:
    root = storage_root.resolve()
    if not root.exists():
        return []
    lock_path = root / ".cleanup.lock"
    with lock_path.open("a") as lock:
        lock_path.chmod(0o600)
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        cutoff = time.time() - retention_hours * 3600
        files = sorted(
            (p for p in root.rglob("*.mkv") if p.is_file() and p.resolve().is_relative_to(root)),
            key=lambda p: p.stat().st_mtime,
        )
        removed: list[Path] = []
        for path in list(files):
            if path.stat().st_mtime < cutoff:
                path.unlink(missing_ok=True)
                removed.append(path)
                files.remove(path)
        required = int(min_free_gb * 1024**3)
        while files and shutil.disk_usage(root).free < required:
            path = files.pop(0)
            path.unlink(missing_ok=True)
            removed.append(path)
        return removed


def _new_output(camera_dir: Path, streams: list[Any]):
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    final = camera_dir / f"{stamp}.mkv"
    counter = 1
    while final.exists() or final.with_suffix(".partial").exists():
        final = camera_dir / f"{stamp}-{counter}.mkv"
        counter += 1
    partial = final.with_suffix(".partial")
    output = av.open(str(partial), mode="w", format="matroska")
    mapping = {stream.index: output.add_stream_from_template(stream) for stream in streams}
    return output, mapping, partial, final


def record_stream(
    source: str,
    camera_name: str,
    storage_root: Path,
    segment_seconds: int,
    stop_after_seconds: float | None = None,
    retention_hours: float | None = None,
    min_free_gb: float = 0,
) -> list[Path]:
    if SAFE_NAME.fullmatch(camera_name) is None:
        raise ValueError("camera name must be a safe slug")
    root = storage_root.resolve()
    camera_dir = (root / camera_name).resolve()
    if not camera_dir.is_relative_to(root):
        raise ValueError("camera output escapes storage root")
    _private_dir(root)
    _private_dir(camera_dir)
    options = {"rtsp_transport": "tcp", "stimeout": "10000000"} if source.lower().startswith("rtsp://") else {}
    completed: list[Path] = []
    started = time.monotonic()
    with av.open(source, mode="r", options=options) as input_container:
        streams = [s for s in input_container.streams if s.type in {"video", "audio"}]
        if not any(s.type == "video" for s in streams):
            raise RuntimeError("source has no video stream")
        output, mapping, partial, final = _new_output(camera_dir, streams)
        segment_started = time.monotonic()
        try:
            for packet in input_container.demux(streams):
                now = time.monotonic()
                if _STOP or (stop_after_seconds is not None and now - started >= stop_after_seconds):
                    break
                if now - segment_started >= segment_seconds and partial.exists() and partial.stat().st_size > 0:
                    output.close()
                    partial.chmod(0o600)
                    partial.replace(final)
                    completed.append(final)
                    if retention_hours is not None:
                        cleanup_recordings(root, retention_hours, min_free_gb)
                    output, mapping, partial, final = _new_output(camera_dir, streams)
                    segment_started = now
                if packet.dts is None or packet.stream.index not in mapping:
                    continue
                packet.stream = mapping[packet.stream.index]
                output.mux(packet)
        finally:
            output.close()
            if partial.exists() and partial.stat().st_size > 0:
                partial.chmod(0o600)
                partial.replace(final)
                completed.append(final)
            else:
                partial.unlink(missing_ok=True)
    return completed


def _write_health(root: Path, camera: str, status: str, **extra: Any) -> None:
    _private_dir(root)
    target = root / f"{camera}.json"
    tmp = target.with_suffix(".tmp")
    payload = {"camera": camera, "status": status, "updated_at": datetime.now(timezone.utc).isoformat(), **extra}
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as handle:
        json.dump(payload, handle, sort_keys=True)
        handle.write("\n")
    tmp.replace(target)


def _stop(_signum, _frame) -> None:
    global _STOP
    _STOP = True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--camera", required=True)
    parser.add_argument("--once-seconds", type=float)
    args = parser.parse_args()
    config = load_config(args.config)
    camera = next((c for c in config.cameras if c.name == args.camera), None)
    if camera is None:
        raise SystemExit(f"unknown camera: {args.camera}")
    source = os.environ.get(camera.url_env)
    if not source:
        raise SystemExit(f"required secret environment variable is missing: {camera.url_env}")
    os.umask(0o077)
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    while not _STOP:
        try:
            segments = record_stream(
                source,
                camera.name,
                config.storage_root,
                config.segment_seconds,
                args.once_seconds,
                config.retention_hours,
                config.min_free_gb,
            )
            cleanup_recordings(config.storage_root, config.retention_hours, config.min_free_gb)
            _write_health(config.health_root, camera.name, "ok", segments_completed=len(segments))
            if args.once_seconds is not None:
                return 0
        except Exception as exc:
            _write_health(config.health_root, camera.name, "reconnecting", error_type=type(exc).__name__)
            if args.once_seconds is not None:
                raise
            time.sleep(5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
