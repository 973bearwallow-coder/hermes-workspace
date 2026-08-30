# Mission Control: verified next implementation

Status observed 2026-08-29

- Canonical service: `mission-control.service`.
- Canonical local endpoint: `http://127.0.0.1:18787/`.
- The service was active and the local endpoint returned HTTP successfully during the audit.
- `hermes dashboard --status` describes the separate Hermes dashboard process and is not authoritative for Mission Control.
- Mission Control already uses one responsive Flask implementation for desktop and phone.
- The live registry currently contains Atlas Voice, Amy, Agents & MoA Board, and Agent Builds. Each app must remain visibly unavailable unless its own configured health check succeeds.

Next bounded implementation

1. Keep one responsive Mission Control source rather than creating separate desktop and phone apps.
2. Add a specialist-status panel sourced from `scripts/specialist_health.py`, showing only READY or BLOCKED from real checks.
3. Keep Talk to Atlas as the primary action and retain the verified Atlas Voice URL from the registry.
4. Keep active work and approvals concise; do not expose credentials, raw logs, or sensitive memory.
5. Preserve per-app health probing and never present an unverified URL as healthy.
6. Add a last-checked timestamp and a manual refresh action.
7. Test desktop and 360-pixel mobile layouts, status API behavior, unavailable-app display, and safe registry validation.

No dashboard implementation change, service restart, gateway restart, or external write is part of this plan.
