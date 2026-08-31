#!/usr/bin/env python3
"""Isolated preflight and benchmark recorder for HunyuanVideo 1.5.

This approved harness does not import or execute the quarantined upstream repository.
Execution is opt-in and uses a caller-supplied model directory.
"""
from __future__ import annotations
import argparse, json, os, shutil, subprocess, time
from pathlib import Path

MIN_FREE_DISK_GIB = 45
MIN_FREE_VRAM_MIB = 14336


def gpu_state():
    cmd = ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu,power.draw", "--format=csv,noheader,nounits"]
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode:
        return {"ok": False, "error": p.stderr.strip(), "returncode": p.returncode}
    fields = [x.strip() for x in p.stdout.splitlines()[0].split(",")]
    return {"ok": True, "name": fields[0], "memory_total_mib": int(fields[1]), "memory_used_mib": int(fields[2]), "memory_free_mib": int(fields[3]), "temperature_c": int(fields[4]), "power_w": float(fields[5])}


def preflight(model_dir: Path, output_dir: Path):
    disk = shutil.disk_usage(output_dir.parent if output_dir.parent.exists() else Path.home())
    gpu = gpu_state()
    reasons = []
    if disk.free < MIN_FREE_DISK_GIB * 1024**3:
        reasons.append("less than 45 GiB free disk")
    if not gpu.get("ok"):
        reasons.append("GPU state unavailable")
    elif gpu["memory_free_mib"] < MIN_FREE_VRAM_MIB:
        reasons.append("less than 14 GiB free VRAM; coexistence gate failed")
    if not model_dir.exists():
        reasons.append("model directory absent")
    return {"ready": not reasons, "reasons": reasons, "disk_free_gib": round(disk.free / 1024**3, 2), "gpu": gpu, "model_dir": str(model_dir), "output_dir": str(output_dir)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, default=Path("models/HunyuanVideo-1.5"))
    ap.add_argument("--output-dir", type=Path, default=Path("outputs"))
    ap.add_argument("--report", type=Path, default=Path("preflight.json"))
    ap.add_argument("--execute", action="store_true", help="Run only after all gates pass")
    args = ap.parse_args()
    report = {"candidate": "HunyuanVideo-1.5 480p I2V step-distilled", "observed_at_epoch": time.time(), "preflight": preflight(args.model_dir, args.output_dir)}
    if args.execute:
        report["execution"] = {"started": False, "reason": "execution adapter intentionally withheld until model files and dependency lock are locally verified"}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["preflight"]["ready"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
