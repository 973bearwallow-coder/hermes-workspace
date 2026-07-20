# Atlas Voice Butler — Detailed Config
_Moved from MEMORY.md during weekly consolidation (2026-07-19)._

## Service
- URL: `https://100.115.214.128:8765` (HTTPS Tailscale, self-signed cert → Chrome Advanced → Proceed; **FIREFOX BLOCKS MIC on self-signed cert, use Chrome**)
- App: `/home/tom/atlas_butler/server.py`, systemd `--user atlas-butler.service`
- Mission Control status view: `http://100.115.214.128:8080` (plain HTTP, no cert warning)
- TTS: Voicebox local (Charles `127.0.0.1:17493`, profile Atlas). NOT Hermes built-in TTS.

## Architecture
- STT: whisper.cpp `ggml-medium.en.bin` (1.53GB, CPU) — upgraded from Parakeet 0.6B 2026-07-19 for accuracy. Bin: `/home/tom/whisper.cpp/build/bin/whisper-cli`.
- Brain: `tencent/hy3:free` (expires 2026-07-21, then auto-switch to `deepseek/deepseek-v4-flash` via cron `eebf2f75fbb8`).
- TTS: Voicebox profile "Atlas" at `127.0.0.1:17493`.
- Latency measured ~9-16s/turn (STT 1.2s + brain 4-9s + TTS 3-6s). Streaming TTS (RealtimeTTS) planned but NOT built — accepted by user, pending.

## 2026-07-18 fixes (hands-free pitfalls #1-#6)
- Clean stream close, onended re-arm, cancelAnimationFrame, AudioContext resume.
- getUserMedia try/catch + visible 'mic blocked' status.
- window.onerror red overlay.
- visibilitychange auto-release mic on app-switch (Android bg tabs hold mic 30-60s → blocks Telegram STT until released).
- Manual 🔓 RELEASE MIC button.
- Root cause of 'buttons dead': self-signed cert + Firefox = getUserMedia blocked → rec undefined → JS crash; fixed by guard + Chrome.

## Wake-word rule
- 'Atlas' REQUIRED only in hands-free (hf:true), matched in first 6 words (fuzzy atlas/atlus/atl). PTT unrestricted.
- Manual RELEASE MIC button + visibilitychange auto-release prevent blocking Telegram STT.

## STT bottleneck history
- VAD threshold 0.02→0.008, silence 1200→2000ms, ffmpeg loudnorm in webm_to_wav.
- Parakeet 0.6B → Whisper medium.en (CPU-only). Telegram transcribes perfectly proving capture was the issue.

## Reference
- Full architecture + latency levers in skill `atlas-voice-butler` (24,021 chars).
