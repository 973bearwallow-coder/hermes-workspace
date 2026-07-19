# 2026-07-17 — Impromptu Builders Guild (Google Meet)

**Source:** Fathom share `_BVdG_4__H6aDYsNBNviRa1sFiiiQ9ss`
**Host:** Rick Rodriguez (rickr1@gmail.com)
**Duration:** 122 min recording (call metadata: 15 min — likely longer session)
**Speakers:** Rick Rodriguez, Ed Grimshaw (UK), Keith Obrosky (Scotland/NY), Yasmine Ison, John Mackenzie, Jobi Armstrong, Elias Siqueira, Lee Grey, Tom Torok

## Summary
Impromptu show-and-tell session. Members demo'd tools they'd built:
- **Tom (Atlas):** Showed the MoA dashboard — 642 models (243 free, 324 cheap, 35 AA-benchmarked), Claude Code + ChatGPT included. Running on **HY3** ("free, at least for a couple more days" — confirms ~Jul 21 promo expiry). Tailscale from phone to access.
- **Keith Obrosky:** Pomodoro timer (WordPress-hosted), teaching/learning ecosystem with lessons + checks.
- **Rick Rodriguez:** Pomodoro timer evolved into client-billing tool (Venmo QR, Zelle, invoice generation, time tracking per project/client).
- **John Mackenzie:** Two major tools — "Business Intelligence Hub" (advisory console, document quality calibration) + "LLM Vault" (multi-provider AI API manager, 590-page spec, governance/provenance at API level). Multi-account, multi-user, multi-provider architecture. Discussed Agent OS vs IDE terminology.
- **Lee Grey:** Feedback on Agent OS as "nebulous term" — argued LLM Vault is closer to an IDE than Agent OS; pushed for transparency in AI decision-making.

## Determinations (actionable intelligence)

### For our stack (VERIFIED)
1. **HY3 free promo expires ~Jul 21** — Tom stated live on call "free, at least for a couple more days" (call was Jul 17). CONFIRMS our finding. DeepSeek V4 Flash already set as post-expiry default. ✅
2. **Tailscale-from-phone pattern is validated by the community** — Rick does it, Yasmine setting it up. Our Charles Tailscale + phone Voicebox access is the right approach. ✅
3. **MoA multi-model dashboard (642 models) resonated with the Guild** — show-and-tell got positive reaction. Our architecture direction is sound. ✅

### Architectural insights (from John's LLM Vault discussion)
4. **Multi-provider + multi-account isolation is a real need** — John runs 2 accounts (same person, different emails) to separate contexts. Our MoA already does multi-provider; consider account-isolation for privacy tiers.
5. **Agent OS vs IDE terminology is contested** — Lee Grey (experienced engineer) finds "Agent OS" nebulous; prefers IDE framing. When explaining our MoA/Atlas stack to technical users, frame as "orchestration IDE" not "Agent OS."
6. **Transparency/provenance in AI decisions = differentiator** — John's 590-page LLM Vault spec emphasizes governance at API level. Our MoA could add decision-logging (which model picked, why) as a future feature.

### Not our use case (noted for context)
- Pomodoro/client-billing tools (Rick/Keith) — practical but not relevant to our food-efficiency / coaching-intel stack.
- WordPress as agent host (Keith) — we use Hermes/OpenClaw, not WP.

## Files
- Transcript: `coaching-calls/2026-07-17-impromptu-guild-transcript.txt` (143 segments, 20,910 chars)
- Keyframes: not generated (no video download; transcript sufficient)
