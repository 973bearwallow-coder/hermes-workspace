# Hermes Desktop App vs Mission Control Dashboard — Comparison
_June 4, 2026 — Atlas analysis_

## Hermes Desktop App (Electron)
**Location:** `~/.hermes/hermes-agent/apps/desktop`
**Launch:** `cd ~/.hermes/hermes-agent/apps/desktop && npx electron .`
**Note:** Requires `sudo chown root:root chrome-sandbox && sudo chmod 4755 chrome-sandbox` first

### Pros
- Polished native desktop GUI (no browser needed)
- Chat with streaming tool output
- Side-by-side preview pane (web pages, files, tool outputs)
- File browser for working directory
- Voice input/output support
- Settings UI for providers, models, tools, credentials
- First-run onboarding wizard
- Built-in self-update mechanism
- Same agent/skills/memory as CLI
- Cross-platform (macOS, Windows, Linux)

### Cons
- Large footprint (~260MB Electron)
- Requires root for sandbox setup on Linux
- Single-user local only (no remote access)
- No system monitoring
- No kanban integration
- No cron job management
- Window display issues on first launch (10x10 pixel window)

## Mission Control Dashboard (Flask)
**Location:** `http://127.0.0.1:18787` (also Tailscale at `http://100.115.214.128:18787`)
**Launch:** systemd service `openclaw-mission`

### Pros
- Lightweight (Python Flask)
- System health monitoring (6 services)
- Native hermes kanban integration
- Activity logs and meeting transcripts
- Remote access via Tailscale (phone-friendly)
- Auto-restart via systemd
- Dark theme
- Accessible from any device on network

### Cons
- Web-based (requires browser)
- No native chat interface
- No file browser
- No voice support
- No built-in onboarding

## Recommendation
**Use both.** Desktop app for daily chat and agent interaction. Mission Control for system oversight, kanban management, and remote monitoring. They complement each other perfectly.

## Integration Opportunities
- Desktop app's chat could be embedded in Mission Control
- Mission Control's system stats could inform Desktop app's status
- Both share the same hermes config and memory
