# Network & Credentials — Detailed Notes
_Moved from MEMORY.md during weekly consolidation (2026-07-19)._

## Tailscale IPs (use Tailscale, NOT ngrok)
- Charles = `100.115.214.128`
- torok (T490s) = `100.106.22.122`, user torok
- Phone = oneplus-10t-5g
- bedroom = `100.108.106.106`

## Google tokens
- TOM = `/home/tom/.hermes/google_tom_token.json` (973bearwallow@gmail.com)
- ATLAS = `/home/tom/.hermes/google/atlas_token.json` (+backups/)
- Daily cron refreshes. Verified live 2026-07-13.

## AI Profit Boardroom (Skool)
- `skool.com/ai-profit-lab-7462`. email = 973bearwallow@gmail.com.
- Coaching calls in Classroom, Fathom recordings. "SKOL"=Skool.
- Chrome on Charles has auto-login cookies.

## Fathom
- `/share/` HTML has call ID + token.
- Transcript = `https://fathom.video/calls/{CALL_ID}/copy_transcript?token={SHARE_TOKEN}`.
- SPOKEN audio only — live chat links NOT in Fathom; use Kimi WebBridge (localhost:10086) for active Chrome tab. Run `check_webbridge.sh` first.

## Subbot memory bridge
- All subbots must: `sys.path.insert(0,'/home/tom/hermes-workspace/memory'); from memory_bridge import get_shared_context, log_subbot`.

## Charles HDMI audio (FIXED 2026-07-18)
- MOK enrolled (pw charles123), nvidia 580.159.03 loads, HDMI sink active.
- PipeWire rule `~/.config/wireplumber/main.lua.d/99-hdmi-audio.lua`.
