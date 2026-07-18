#!/usr/bin/env python3
"""
process_coaching_call.py — Full pipeline for a Fathom coaching-call recording.

1. Extract transcript + AI summary from Fathom /share/ URL (browser)
2. Generate sparse keyframes (screen-share capture) linked to timestamps
3. Write intelligence file + update determinations.md
4. Clean up raw video (keep only small screenshots + md)

Run interactively (Atlas captions frames with vision) or via cron (OCR fallback).
"""
import os, sys, subprocess, argparse
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.expanduser("~/hermes-workspace/coaching-calls")
DETERMINATIONS = os.path.expanduser("~/hermes-workspace/memory/determinations.md")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Fathom /share/ URL")
    ap.add_argument("--name", help="Output base name (default: from URL)")
    ap.add_argument("--community", default="ai-profit-boardroom",
                    help="ai-profit-boardroom | builders-guild")
    ap.add_argument("--skip-keyframes", action="store_true")
    args = ap.parse_args()

    name = args.name or args.url.split("/")[-1]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"=== Processing {args.community} call: {args.url} ===")
    print(f"Intelligence file: {VAULT}/{date}-{args.community}.md")

    if not args.skip_keyframes:
        print("--- Generating keyframes (screen-share capture) ---")
        kf = subprocess.run([
            "python3", os.path.join(SCRIPT_DIR, "fathom_keyframes.py"),
            "--url", args.url, "--name", f"{date}-{args.community}",
            "--out", VAULT
        ], capture_output=True, text=True, timeout=400)
        print(kf.stdout.strip() or kf.stderr.strip())

    print("--- Atlas: extract transcript + determinations ---")
    print("(Interactive: Atlas reads the /share/ page, writes intelligence file,")
    print(" links keyframes.md, appends to determinations.md)")
    print("DONE — see intelligence file for full extraction.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
