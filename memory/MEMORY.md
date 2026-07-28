# MEMORY.md — Atlas Long-Term Memory

> Lean index. Project details live in `/home/tom/Documents/ObsidianVault/`.
> Protocols: `atlas-protocols.md` (in `.hermes/workspace/memory/`)

## Who Tom Is
- **Tom Torok**, 61, Falls Church VA (22042)
- Co-owner of Paw Prints pet services (Jane is primary owner/face)
- Hermes v0.16.0, Charles OpenClaw v2026.6.1, Qwen 2.5 7B on RTX 3090
- Models: DeepSeek V4 Flash (primary), tencent/hy3 (fallback)
- Hobbies: AI, woodworking, vehicles, guns, fishing, hunting, hiking, fitness, cooking
- Wife: Jane | Mother-in-law: Caroline (turned 90, June 6 2026)

## Active Ecosystem
- Atlas (Hermes) ↔ Charles (OpenClaw) ↔ Obsidian Vault
- Daily cron 6am: memory audit (job 92cc84ba0deb)
- Mission Control: localhost:18787

## Key Preferences
- No auto model switching — Tom says "switch models" explicitly
- Stay off Gemini 2.5 Flash — fallback is tencent/hy3
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
- Full details: `Tools/voicebox-local-ai-voice.md`

## Obsidian Vault Pointers
- Projects: `ObsidianVault/Projects/` (Shot-Clock, Pool-Referee, Price-Tracking, Paw-Prints)
- Areas: `ObsidianVault/Areas/` (Coaching, Technology)
- Brand master ref: `ObsidianVault/Projects/Paw-Prints/Brand-Brain.md`
- Business brief: `ObsidianVault/Projects/Paw-Prints/Business-Brief.md`
- Coaching insights (AI Profit Boardroom): `ObsidianVault/Areas/Coaching/insights.md`
- GitHub tools inventory: `ObsidianVault/Areas/Technology/github-tools.md`
- Hermes/Charles config: `ObsidianVault/Areas/Technology/hermes-config.md`

## Pending / Recent
- Pool Referee: Raspberry Pi sourced (George Sandy, $75 Annandale) — awaiting pickup. NexiGo N60 camera. ThinkPad X1 ($119) as possible laptop compute.
- Duke's Shot Clock v5: live, Voicebox integrated
- Dishwasher: LG LDTH5554S open-box $419.99 bought for TNDC pool hall (per Price-Tracking notes)
- Brand Brain: last updated 2026-06-23 (master ref for Paw Prints work)

---
_Capacity target: <8K chars. Last consolidated: 2026-07-27_
