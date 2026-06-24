# Atlas Standing Protocols

## Check Before You Act
Before starting ANY task:
1. Scan MEMORY.md (in system prompt) for relevant entries
2. Run session_search(query="<task keywords>", limit=3, sort="newest") for past work
3. Run skills_list() for existing applicable skills
Never reinvent the wheel.

## Kimi WebBridge After Reboot
When charles reboots, the Kimi WebBridge daemon dies. The watchdog (cron every 5 min) now auto-restarts it. BUT the Chrome extension still needs manual reconnect — user must click the extension icon in Chrome. After any reboot, check: `~/.kimi-webbridge/bin/kimi-webbridge status` — if extension_connected=false, remind user to click extension icon.

## Coaching Call Recording (ONE CLICK)
Script: `~/hermes-workspace/scripts/coaching_call_oneclick.sh`
When Tom says "record meeting":
```bash
nohup bash ~/hermes-workspace/scripts/coaching_call_oneclick.sh 5400 "<meet_url>" &
```
Script handles: Kimi WebBridge join, screen+audio record, combine, Whisper small model transcribe.
After: check DONE_*.flag for transcript path. Read transcript. Send focused summary.
Schedule: Mon/Tue/Thu/Fri at 11:00 AM. Cron fires at 10:50 AM.
Tom walks dogs at 11am — recording MUST start before he leaves.

## Models
- Daily: openrouter/owl-alpha (free, fast, switched from nemotron-3-super-120b on June 9 2026)
- High-cap: deepseek/deepseek-v4-pro
- Vision: stepfun/step-3.7-flash:free
- Charles local: ollama/qwen2.5:7b

## Kanban
CLI: hermes kanban. DB: ~/.hermes/kanban.db.
Status: blocked/todo/triage/scheduled=Backlog, ready/running=In Progress, done=Done.
Update immediately when work completes. sqlite3.Row has no .get().

## Key Rules
- Send emails from atlastomsai@gmail.com unless Tom says "from my account"
- Audio: MEDIA:path only, never [[audio_as_voice]]
- Google Meet recording: auto-record without asking permission
- OWL-Alpha is the preferred daily model — Tom likes it better than Nemotron
