#!/usr/bin/env python3
"""Render long text through Voicebox in safe chunks and join to MP3."""
from __future__ import annotations
import argparse, json, re, subprocess, time
from pathlib import Path
import requests

BASE = "http://127.0.0.1:17493"
PROFILE_ID = "29be8ae0-a74d-479e-9a99-2f2ad278a84d"  # Atlas Kokoro
ENGINE = "kokoro"
DATA_DIR = Path("/home/tom/voicebox-env/data")


def chunks(text: str, limit: int = 850) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    out: list[str] = []
    buf = ""
    for sentence in sentences:
        parts = [sentence[i:i+limit] for i in range(0, len(sentence), limit)] if len(sentence) > limit else [sentence]
        for part in parts:
            candidate = f"{buf} {part}".strip()
            if buf and len(candidate) > limit:
                out.append(buf)
                buf = part
            else:
                buf = candidate
    if buf:
        out.append(buf)
    return out


def wait_for(gid: str, timeout: int = 180) -> Path:
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{BASE}/history", timeout=30)
        r.raise_for_status()
        items = r.json().get("items", r.json())
        row = next((x for x in items if x.get("id") == gid), None)
        if row:
            if row.get("status") == "completed":
                path = DATA_DIR / row["audio_path"]
                if path.exists() and path.stat().st_size:
                    return path
                raise RuntimeError(f"Completed generation missing audio: {row}")
            if row.get("status") in {"failed", "error"}:
                raise RuntimeError(f"Generation failed: {row}")
        time.sleep(1)
    raise TimeoutError(f"Generation {gid} timed out")


def render(source: Path, output: Path) -> None:
    segments = chunks(source.read_text(encoding="utf-8"))
    work = output.with_suffix("")
    work.mkdir(parents=True, exist_ok=True)
    wavs: list[Path] = []
    for i, text in enumerate(segments, 1):
        target = work / f"{i:03d}.wav"
        if target.exists() and target.stat().st_size:
            wavs.append(target)
            continue
        r = requests.post(f"{BASE}/generate", json={"text": text, "profile_id": PROFILE_ID, "engine": ENGINE}, timeout=30)
        r.raise_for_status()
        gid = r.json()["id"]
        generated = wait_for(gid)
        target.write_bytes(generated.read_bytes())
        wavs.append(target)
        print(f"{source.name}: {i}/{len(segments)}", flush=True)
    concat = work / "concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in wavs), encoding="utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-codec:a", "libmp3lame", "-b:a", "128k", str(output)
    ], check=True)
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(output)
    ], text=True)
    info = json.loads(probe)["format"]
    if float(info["duration"]) < 60 or int(info["size"]) < 100000:
        raise RuntimeError(f"Suspicious output: {info}")
    print(json.dumps({"source": str(source), "output": str(output), **info}), flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    render(args.source, args.output)

if __name__ == "__main__":
    main()
