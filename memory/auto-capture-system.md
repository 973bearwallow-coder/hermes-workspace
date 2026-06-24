# Auto-Capture System — Architecture Notes
# Built: June 9 2026

## What It Does
Linux-native replacement for OMI (macOS-only). Three capture pipelines that auto-save to Obsidian:

1. **Audio → Whisper → Obsidian**: Records from USB mic in chunks, transcribes, saves to daily notes
2. **Chat Sessions → Obsidian**: Watches Hermes session files, syncs conversations to daily notes
3. **Screen OCR → Obsidian**: Periodic screenshots, extracts text, saves meaningful changes

## File Structure
```
~/hermes-workspace/scripts/auto-capture/
├── audio_capture.py              # Audio recorder + Whisper transcriber
├── chat_sessions_to_obsidian.py  # Hermes session watcher/syncer
├── screen_ocr.py                 # Screen capture + OCR
├── audio_cache/                  # Temporary WAV files (auto-cleaned)
├── chat_sync_state.json          # Tracks processed sessions
└── screen_ocr_state.json         # Tracks last screen hash (dedup)

~/.config/systemd/user/
├── auto-capture-audio.service    # Audio capture service
├── auto-capture-chat.service     # Chat sync service
└── auto-capture-screen.service   # Screen OCR service

~/Documents/ObsidianVault/Captures/
├── Audio/YYYY-MM-DD.md           # Daily audio transcripts
├── Chat/YYYY-MM-DD.md            # Daily chat sessions
└── Screen/YYYY-MM-DD.md          # Daily screen captures
```

## Service Management
```bash
# Check status
systemctl --user status auto-capture-{audio,chat,screen}.service

# Stop/start
systemctl --user stop auto-capture-audio.service
systemctl --user start auto-capture-audio.service

# View logs
journalctl --user -u auto-capture-audio.service -f
```

## Default Intervals
- Audio: Record 30s every 60s (configurable)
- Chat: Check for new sessions every 5 min
- Screen: Screenshot every 2 min, save if changed (5 min min interval between saves)

## Manual Testing
```bash
# Audio (5s test)
source ~/.hermes/hermes-agent/venv/bin/activate
python3 scripts/auto-capture/audio_capture.py --once --duration 5

# Chat (force re-sync all)
python3 scripts/auto-capture/chat_sessions_to_obsidian.py --force-all

# Screen (single capture)
DISPLAY=:1 python3 scripts/auto-capture/screen_ocr.py --once
```

## Key Design Decisions
- Chose not to install OMI (macOS 14+ / Xcode / Swift requirement, won't run on Linux)
- Used ImageMagick `import` for screenshots (already installed, no extra deps)
- Used Tesseract OCR (already installed)
- Used Whisper CLI (already installed, small model)
- Services auto-start on boot, restart on failure
- All three pipelines write to dated daily notes in Obsidian for easy browsing
