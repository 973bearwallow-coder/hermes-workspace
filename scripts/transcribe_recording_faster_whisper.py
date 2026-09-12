#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("output_base")
parser.add_argument("--model", default="medium.en")
args = parser.parse_args()
out = Path(args.output_base)
out.parent.mkdir(parents=True, exist_ok=True)
model = WhisperModel(args.model, device="cuda", compute_type="int8_float16")
segments_iter, info = model.transcribe(
    args.input,
    language="en",
    vad_filter=True,
    beam_size=5,
    condition_on_previous_text=True,
)
segments = [
    {"start": s.start, "end": s.end, "text": s.text.strip()}
    for s in segments_iter if s.text.strip()
]
text = " ".join(s["text"] for s in segments)
out.with_suffix(".txt").write_text(text + "\n", encoding="utf-8")
out.with_suffix(".json").write_text(json.dumps({
    "text": text,
    "language": getattr(info, "language", "en"),
    "language_probability": getattr(info, "language_probability", None),
    "segments": segments,
}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"segments": len(segments), "characters": len(text), "output": str(out)}))
