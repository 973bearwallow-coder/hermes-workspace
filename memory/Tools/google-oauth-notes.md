# Google OAuth & Email — Detailed Notes
_Created: June 2026. Moved from MEMORY.md during weekly consolidation._

## Accounts (both done as of June 3 2026)
- Atlas: atlastomsai@gmail.com → token at ~/.hermes/google/atlas_token.json
- Tom: 973bearwallow@gmail.com → token at ~/.hermes/google/token.json
- Format: JSON tokens (not pickle).

## Token Management
- Auto-refresh cron: 6am daily.
- Token manager: google_token_manager.py.
- Quick CLI: gws script.
- OAuth env: BROWSER=/usr/bin/google-chrome-stable DISPLAY=:1.
- Client secret: one-time download only.

## Email Rules
- Default send: atlastomsai@gmail.com.
- Only use Tom's account if he explicitly says "from my account" or "send from my account".
- Only notify Tom about emails if something urgent needs action.
- Monitor Tom's inbox for shipping notifications.

## Email Organization (created Jun 13 2026)
See: memory/business/email-organization.md
- Folders: Appointments (1mo), Farm (1mo), Guns (2wk), News (1wk), Promotions (1wk), Tools (1wk).
