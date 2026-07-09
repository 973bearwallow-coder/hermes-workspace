# MEMORY.md — Atlas Long-Term Memory

> Lean index. Project details live in `/home/tom/Documents/ObsidianVault/`.
> Protocols: `atlas-protocols.md` (in `.hermes/workspace/memory/`)

## Who Tom Is
- **Tom Torok**, 61, Falls Church VA (22042)
- Co-owner of Paw Prints pet services (Jane is primary owner/face)
- Hermes v0.16.0, Charles OpenClaw v2026.6.1, Qwen 2.5 7B on RTX 3090
- Models: OWL-Alpha (default), DeepSeek V4 Pro (heavy reasoning), Nemotron 3 Nano (free backup)
- Hobbies: AI, woodworking, vehicles, guns, fishing, hunting, hiking, fitness, cooking
- Wife: Jane | Mother-in-law: Caroline (turned 90, June 6 2026)

## Active Ecosystem
- Atlas (Hermes) ↔ Charles (OpenClaw) ↔ Obsidian Vault
- Daily cron 6am: memory audit (job 92cc84ba0deb)
- Mission Control: localhost:18787

## Key Preferences
- No auto model switching — Tom says "switch models" explicitly
- Vision model: llama3.2-vision:11b local Ollama (use API directly, not tool — broken 401)
- Email: use `atlastomsai@gmail.com` default
- Theme: dark
- Communication: professional, direct, voice-ready
- Voicebox is default TTS/voice-cloning/STT tool (replaced Resemble.AI $14/mo + Super Whisper Flow $15/mo → free on 3090)

## Voicebox
- Server: `127.0.0.1:17493`, auto-starts via systemd
- Profile: "Atlas" (Chatterbox engine)
- TTS: text→speech (3s for typical phrase)
- STT: Whisper base model on GPU (3.5s for typical clip)
- Voice cloning: upload sample, generate speech in that voice
- Code fix applied 2026-06-27: Whisper loading via `whisper.load_model()` instead of HF direct
- Env: `/home/tom/voicebox-env/`
- ⚠️ Cancel Resemble.AI $14/mo subscription
- Full details: `Tools/voicebox-local-ai-voice.md`

## Obsidian Vault Pointers
- Projects: `ObsidianVault/Projects/` (Shot-Clock, Pool-Referee, Price-Tracking, Paw-Prints)
- Areas: `ObsidianVault/Areas/` (Coaching, Technology)
- Brand master ref: `ObsidianVault/Projects/Paw-Prints/Brand-Brain.md`
- Business brief: `ObsidianVault/Projects/Paw-Prints/Business-Brief.md`
- Coaching insights (AI Profit Boardroom): `ObsidianVault/Areas/Coaching/insights.md`
- GitHub tools inventory: `ObsidianVault/Areas/Technology/github-tools.md`
- Hermes/Charles config: `ObsidianVault/Areas/Technology/hermes-config.md`

## Pending / Recent (June 2026)
- Pool Referee: Raspberry Pi sourced (George Sandy, $75 Annandale) — waiting for seller meet-up. NexiGo N60 camera added to setup.
- Duke's Shot Clock v5: live on GitHub Pages, Voicebox integrated for audio
- Brand Brain: last updated 2026-06-23 (master reference for all Paw Prints work)
- Travel camera for Jane: Panasonic Lumix ZS80/TZ95 recommended (30x zoom, 20.3MP, $500-800 range)
- TNDC Pam Bondi invite: IP-Adapter FaceID pipeline for likeness (CLIP ViT encoder needed)
- Dishwasher pickup (LG, ~$420)
- ZenBook if ThinkPad ghosted

---
_Capacity target: <8K chars. Last consolidated: 2026-07-08_
