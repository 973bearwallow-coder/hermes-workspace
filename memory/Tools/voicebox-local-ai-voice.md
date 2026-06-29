# Voicebox — Local AI Voice Studio

## Overview
Voicebox is our default TTS, voice cloning, and STT solution running locally on the RTX 3090. It replaced:
- **Resemble.AI ChatterboxTTS** ($14/mo) — Tom cancelled the subscription 2026-06-27
- **Super Whisper Flow** ($15/mo) — no longer needed

**Net savings: $29/mo. Runs free on existing 3090 hardware.**

## Server Details
- **URL:** `http://127.0.0.1:17493`
- **Profile:** "Atlas" (Chatterbox engine)
- **Auto-start:** systemd service
- **Environment:** `/home/tom/voicebox-env/`
- **GPU:** NVIDIA RTX 3090 (CUDA)

## API Endpoints
| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Status + GPU info |
| `/generate` | POST | TTS (text → speech) |
| `/history` | GET | Check generation status/results |
| `/transcribe` | POST | STT (speech → text) |

### TTS Request Format
```json
{
  "text": "Your text here",
  "profile_id": "8d2273da-db34-453a-9ae4-05e051d767d5",
  "engine": "chatterbox"
}
```

### STT Request Format
```bash
curl -X POST http://127.0.0.1:17493/transcribe \
  -F "file=@audio.wav" \
  -F "model=base"
```

## Performance (verified 2026-06-27)
| Operation | Duration |
|---|---|
| TTS (short phrase) | ~3.08s |
| STT (zinger_1.wav) | ~3.5s |
| Health check | instant |

## Code Fix Applied (2026-06-27)
**Bug:** Whisper STT backend had weight-loading issue for output projection layer.

**Fix** (in `pytorch_backend.py` line ~299):
1. Load Whisper via `whisper.load_model()` instead of `WhisperForConditionalGeneration.from_pretrained()`
2. Store as `self._whisper_model` (separate from `self.model` which TTS uses for Qwen3TTSModel)
3. Simplified `_transcribe_sync()` to use `self._whisper_model.transcribe()` directly

**Verification:** End-to-end tests passed (TTS ✅, STT ✅, Health ✅)

## Usage Notes
- Always prefer Voicebox over built-in TTS tools (text_to_speech)
- Voice cloning: upload a voice sample to generate speech in that voice
- Transcribe audio files via Whisper base model on GPU
- After charles reboot: check `systemctl status voicebox` to ensure it's running

## Pitfalls
- Server must be running before TTS/STT requests
- Whisper STT uses `lazy loading` — first request is slower (model loads on demand)
- If STT returns errors, check: `curl http://127.0.0.1:17493/health` for status
