# Hermes Desktop App — Launch & Troubleshooting
_Created: June 2026. Moved from MEMORY.md during weekly consolidation._

## Launch
```bash
cd ~/.hermes/hermes-agent/apps/desktop
npx electron .
```
- MUST use `terminal(background=true, ...)` — do NOT use `&` inside foreground terminal commands.
- Requires sandbox fix: `sudo chown root:root chrome-sandbox && sudo chmod 4755 chrome-sandbox`

## Window Issues
- Window may render at 10×10 pixels on first launch.
- Fix: `DISPLAY=:1 xdotool search --name "Hermes" && xdotool windowactivate <id>`

## Customization (done Jun 4 2026)
- Added Mission Control dashboard button (dashboard icon) in titlebar between mute and settings.
- Opens http://localhost:18787 in browser.
- .desktop launchers created on ~/Desktop/ and in applications menu for both "Hermes Desktop" and "Mission Control".

## Workflow
- Telegram = primary daily chat.
- Desktop app = session history review + file preview.
- Mission Control = system oversight.
- All three are complementary.
