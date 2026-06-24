# AI Profit Boardroom — Key Findings for Tom
# Researched: June 9 2026 via Kimi WebBridge

## 1. THE INFINITE CONTEXT ENGINE (May 11)
**How it works:**
- **Capture**: OMI app records everything (mic + screen) in background
- **Organise**: OMI processes recordings into structured memory notes
- **Store**: Obsidian holds the memory vault locally (free, private)
- **Deploy**: Any AI agent reads the vault via file path

**The Stack:**
1. OMI (free) — background recording → omi.me
2. Obsidian (free) — note storage/second brain → obsidian.md
3. Hermes Agent — reads vault via file path for persistent context

**Setup:**
- Install OMI + grant mic/screen permissions
- Install Obsidian + create vault
- Connect OMI → Obsidian (export destination)
- In Claude/Hermes: "Use this file path for memory: /path/to/vault/OMI_Memories.md"
- Works with Hermes, OpenClaw, Claude Code — all share same vault

**Key insight from their community post:**
"Your AI agent wakes up every day already knowing everything about you."

**Status: WE ALREADY HAVE THIS SETUP!**
- Obsidian vault at ~/Documents/ObsidianVault
- Need to: Install OMI and connect it to the vault

## 2. HERMES + OBSIDIAN MCP (May 13)
**The Goldie Delegation Loop:**
- Claude (brain) → MCP bridge (connector) → Hermes (hands)
- GitHub: https://github.com/mlennie/claude-hermes-mcp
- Lets Claude Desktop/mobile send tasks to local Hermes Agent
- Hermes can: browse web, send emails, create docs, schedule, message

**Key insight:** Without MCP bridge, every task Claude suggests still requires YOU to execute. With MCP, Claude hands directly to Hermes.

**For Paw Prints:**
- Auto email summaries inbox
- Schedule recurring tasks
- Web research on competitors
- Document creation (reports, SOPs)
- Persistent memory of client preferences

**Status: WE HAVE MCP CAPABILITY!**
- Hermes already supports MCP
- Need to: set up claude-hermes-mcp bridge

## 3. AGENT OS (Ongoing course)
**8-prompts to build Mission Control dashboard:**
1. Create dashboard (Next.js + Tailwind + Framer Motion) via Claude Code
2. Make it beautiful + per-agent pages
3. Add voice input (browser built-in, no API keys)
4. Save to Obsidian vault (auto daily files)
5. Goals + Journal (checkbox tasks, daily entries)
6. Debug (tell Claude what broke)
7. Make portable (config file + setup wizard)
8. Generate shareable guide

**Their version vs ours:**
- Theirs: Next.js + Tailwind + Framer Motion (more polished)
- Ours: Flask (functional but simpler)
- Theirs has: voice input, Obsidian auto-save, goals tracking

**Status: WE HAVE MISSION CONTROL!**
- Could upgrade with: voice input, Obsidian auto-save integration

## 4. VOICE SYSTEM
From Agent OS Prompt #3:
"Add a mic button to every chat box. Click to talk and have speech turn into text using the browser's built-in voice recognition. No API keys."

This is FREE — uses browser's built-in Web Speech API.
Works in Chrome/Safari without any API keys.

**For Paw Prints:**
- Add voice input to Mission Control dashboard
- Could enable voice commands for Atlas

## 5. WHAT MAKES THEIR HERMES "NEVER FORGET"
It's a combination of:
1. **OMI auto-capture** — records everything automatically
2. **Obsidian vault** — single shared brain, locally stored
3. **File path reference** — all agents point to same vault
4. **Auto-notes** — AI writes notes, not the human
5. **30-day buildup system** — structured onboarding that feeds the vault

**Their exact quote:** "Stop training your AI every morning. Start letting your AI train itself on you."

## 6. ACTION ITEMS FOR US

### Immediate (free, do today):
1. Install OMI (omi.me) — connect to our Obsidian vault
2. Test voice input in Mission Control dashboard (Web Speech API)
3. The Obsidian vault is already set up and working

### Short-term (this week):
1. Set up claude-hermes-mcp bridge (GitHub: mlennie/claude-hermes-mcp)
2. Add auto-save from Hermes to Obsidian (like their Agent OS)
3. Create "About Paw Prints" note in vault as brand brain

### Key Paw Prints application:
- Brand brain: feed 6 months of notes to AI → it writes in YOUR voice
- Client memory: auto-save client interactions to vault
- Content engine: "Read my vault, write 5 posts that sound like me"
- Goal tracking: daily priorities based on vault goals

## 7. WHAT WE ALREADY HAVE THAT THEY DON'T
- Dual GPU setup (RTX 3090)
- Local Ollama models
- Kimi WebBridge for browser automation
- Telegram integration
- Coaching call recording pipeline
- Stable Diffusion locally

## 8. WHAT THEY HAVE THAT WE DON'T
- OMI auto-capture (background recording → Obsidian)
- Claude-Hermes MCP bridge (Claude can trigger Hermes tasks)
- Structured 30-day onboarding system
- Voice input in dashboard
- Auto-save all chats to Obsidian
