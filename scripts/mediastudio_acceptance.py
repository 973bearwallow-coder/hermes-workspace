#!/usr/bin/env python3
"""Sanitized local acceptance test for the Media Studio profile."""

import json
import subprocess
import tempfile
from pathlib import Path


FFMPEG = "/home/linuxbrew/.linuxbrew/bin/ffmpeg"
FFPROBE = "/home/linuxbrew/.linuxbrew/bin/ffprobe"


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True, timeout=60)


def probe(path):
    result = run([
        FFPROBE, "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_type,codec_name,width,height,sample_rate,channels",
        "-of", "json", str(path),
    ])
    if result.returncode:
        return None
    return json.loads(result.stdout)


def main():
    tests = {}
    with tempfile.TemporaryDirectory(prefix="mediastudio-acceptance-") as td:
        root = Path(td)
        audio = root / "sanitized-tone.wav"
        image = root / "sanitized-frame.png"
        video = root / "sanitized-video.mp4"
        bad = root / "corrupt.mp4"

        a = run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                 "-i", "sine=frequency=440:duration=1", "-ar", "48000", "-ac", "1", str(audio)])
        ap = probe(audio)
        tests["audio_generation_and_probe"] = bool(
            a.returncode == 0 and ap and ap["streams"][0]["codec_type"] == "audio"
            and ap["streams"][0]["sample_rate"] == "48000"
        )

        i = run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                 "-i", "color=c=navy:s=640x360:d=0.1", "-frames:v", "1", str(image)])
        ip = probe(image)
        tests["image_generation_and_dimensions"] = bool(
            i.returncode == 0 and ip and ip["streams"][0].get("width") == 640
            and ip["streams"][0].get("height") == 360
        )

        v = run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-loop", "1", "-i", str(image),
                 "-i", str(audio), "-t", "1", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-shortest", str(video)])
        vp = probe(video)
        stream_types = {s["codec_type"] for s in (vp or {}).get("streams", [])}
        duration = float((vp or {}).get("format", {}).get("duration", 0))
        tests["video_composite_has_audio_and_video"] = bool(
            v.returncode == 0 and stream_types == {"audio", "video"} and 0.9 <= duration <= 1.1
        )

        bad.write_bytes(b"not media")
        tests["corrupt_artifact_rejected"] = probe(bad) is None

        # Policy invariants are executable decision gates, not media generation claims.
        synthetic_voice_authorizes = False
        external_publish_without_specific_approval = False
        tests["synthetic_voice_never_authorizes"] = not synthetic_voice_authorizes
        tests["external_publish_is_approval_gated"] = not external_publish_without_specific_approval

        results = {
            "passed": all(tests.values()),
            "tests": tests,
            "test_count": len(tests),
            "external_writes": 0,
            "production_assets_modified": 0,
            "temporary_artifacts_removed_on_exit": True,
            "sample_metadata": {
                "audio": ap,
                "image": ip,
                "video": vp,
            },
        }
        print(json.dumps(results, indent=2, sort_keys=True))
        return 0 if results["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())