#!/usr/bin/env python3
"""
latency_monitor.py — Weekly latency check + auto-promotion.

Runs the latency probe on the key MoA models, compares against the butler's
CURRENT STT model and brain, and if a substantially faster option exists,
writes a recommendation flag to /home/tom/hermes-workspace/memory/latency_alert.json
for Atlas to act on (or auto-swaps if clearly better + safe).

Design:
- STT: compares whisper.cpp model load+transcribe time. If a smaller/faster
  ggml model benchmarks >30% faster with acceptable accuracy, flag it.
- Brain: compares catalog latency_ms for the current brain vs alternatives.
- Emits a Telegram-friendly summary if anything changed.

Safety: NEVER auto-swaps STT to a model we haven't accuracy-tested. Only FLAGS
for Atlas review. Brain swaps are lower-risk (text only) so can auto-promote
if >20% faster and from a trusted provider.
"""
import sys, os, json, time, subprocess, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import moa_router as MR
import moa_dashboard as MD
import moa_catalog as MC

MEM = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEM, "model_catalog.json")
ALERT = os.path.join(MEM, "latency_alert.json")

# Current butler config (read from atlas_desk if available, else defaults)
try:
    sys.path.insert(0, "/home/tom/atlas_butler")
    import atlas_desk as A
    CURRENT_STT = os.path.basename(A.PARAKEET_MODEL)
    CURRENT_BRAIN = A.BRAIN_LADDER[0]["id"] if A.BRAIN_LADDER else "tencent/hy3:free"
except Exception:
    CURRENT_STT = "ggml-small.en.bin"
    CURRENT_BRAIN = "openai-codex/gpt-5.6-sol"

def probe_stt(model_path):
    """Time a whisper.cpp transcribe on a 3s synthetic clip."""
    if not os.path.exists(model_path):
        return None
    sr = 16000; dur = 3
    import numpy as np, struct
    t = np.linspace(0, dur, sr * dur)
    sig = (np.sin(2 * np.pi * (80 + 160 * t) * t) * 0.3).astype(np.float32)
    wav = b"".join(struct.pack("<h", int(s * 32767)) for s in sig)
    wav_bytes = (b"RIFF" + struct.pack("<I", len(wav) + 36) + b"WAVEfmt " +
                 struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16) +
                 b"data" + struct.pack("<I", len(wav)) + wav)
    wf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wf.write(wav_bytes); wf.close()
    binp = "/home/tom/whisper.cpp/build/bin/whisper-cli"
    t0 = time.perf_counter()
    try:
        subprocess.run([binp, "-m", model_path, "-f", wf.name, "-nt", "-ps", "1"],
                       capture_output=True, timeout=60)
        return time.perf_counter() - t0
    except Exception:
        return None
    finally:
        os.unlink(wf.name)

def main():
    catalog = json.load(open(CATALOG))
    models = {m["id"]: m for m in catalog["models"]}

    # --- BRAIN: find fastest trusted brain candidate ---
    brain_cands = [m for m in catalog["models"]
                   if m.get("tier") in ("free", "cheap", "premium")
                   and m.get("modalities", {}).get("text")
                   and m.get("latency_ms")]
    brain_cands.sort(key=lambda m: m["latency_ms"])
    fastest_brain = brain_cands[0] if brain_cands else None

    # --- STT: probe available ggml models ---
    models_dir = "/home/tom/whisper.cpp/models"
    ggml = [f for f in os.listdir(models_dir) if f.startswith("ggml-") and f.endswith(".bin")]
    stt_results = {}
    for g in ggml:
        if "small" in g or "medium" in g or "base" in g or "tiny" in g:
            dt = probe_stt(os.path.join(models_dir, g))
            if dt:
                stt_results[g] = round(dt, 1)

    # --- Compare ---
    alert = {"ts": time.time(), "stt": {}, "brain": {}, "recommend": []}

    # STT: flag if a faster model exists (>25% faster than current)
    cur_stt_dt = stt_results.get(CURRENT_STT)
    if cur_stt_dt:
        for g, dt in stt_results.items():
            if g != CURRENT_STT and dt < cur_stt_dt * 0.75:
                alert["recommend"].append(
                    f"STT {g} is {round((cur_stt_dt-dt)/cur_stt_dt*100)}% faster ({dt}s vs {cur_stt_dt}s) — verify accuracy before swap")
    alert["stt"] = {"current": CURRENT_STT, "current_dt": cur_stt_dt, "all": stt_results}

    # Brain: auto-promote if >20% faster and trusted provider
    if fastest_brain and fastest_brain["id"] != CURRENT_BRAIN:
        cur_brain_dt = models.get(CURRENT_BRAIN, {}).get("latency_ms")
        if cur_brain_dt and fastest_brain["latency_ms"] < cur_brain_dt * 0.8:
            trusted = fastest_brain["home_provider"] in ("openai-codex", "openrouter", "agnes")
            alert["recommend"].append(
                f"BRAIN {fastest_brain['id']} is {round((cur_brain_dt-fastest_brain['latency_ms'])/cur_brain_dt*100)}% faster — {'AUTO-SWAP OK' if trusted else 'review needed'}")
            if trusted:
                alert["brain_auto_swap"] = fastest_brain["id"]

    json.dump(alert, open(ALERT, "w"), indent=2)

    # Stdout summary (cron delivers this)
    print(f"=== Weekly Latency Monitor ({time.strftime('%Y-%m-%d')}) ===")
    print(f"STT current: {CURRENT_STT} @ {cur_stt_dt}s" if cur_stt_dt else f"STT current: {CURRENT_STT}")
    for g, dt in sorted(stt_results.items(), key=lambda x: x[1]):
        print(f"  {dt:5.1f}s  {g}")
    print(f"Brain current: {CURRENT_BRAIN}")
    if fastest_brain:
        print(f"  fastest: {fastest_brain['id']} @ {fastest_brain['latency_ms']}ms")
    if alert["recommend"]:
        print("\nRECOMMENDATIONS:")
        for r in alert["recommend"]:
            print(f"  - {r}")
    else:
        print("\nNo faster options found — current config is optimal.")

if __name__ == "__main__":
    main()
