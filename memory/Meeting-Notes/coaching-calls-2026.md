# Coaching Calls — 2026 Archive Notes
_Consolidated from MEMORY.md during weekly memory consolidation, June 21 2026._

## Workflow (updated June 16)
- Recording cron removed. Post-call review cron (Tue/Fri 1pm) picks up tl;dv transcript → summarizes → delivers
- Fathom + Whisper for archive transcription
- Gap: No automated pickup of Boardroom Fathom links on Mon/Thu call days
- User wants Fathom links pasted manually → Atlas downloads + transcribes

## June 18, 2026 Call Summary
**Source:** tl;dv (Gmail ID 77714), AI Profit Boardroom coaching call
**Participants:** Rashad, Tim (Malaysia), Yasmine, Ryan + others

**Action Items:**
- Yasmine → connect with Tim on dentist scheduling project
- Tim → download Claude Desktop + Claude Code CLI setup
- Rashad → updates on car dealership AI implementation

**Key Takeaways:**
- Claude = planning, Hermes = execution (matches how Tom uses Atlas)
- Agents augment human decision-making, don't replace oversight
- Match tools to use cases — don't force AI where it doesn't fit
- Agent-to-agent communication without disk writes needs capture for audit/compliance
- Separate chats per project phase = good context management practice

**Business Context:**
- Tim has 3 Go High Level accounts ($97/mo) — potential revenue
- Dentist scheduling project → Gemini + Twilio integration
- Short market window for AI-enabled solutions

## Coaching Call Review Gap (2026-06-16) — RESOLVED/SUPERSEDED
- Coaching Call Review cron (619b9a31d107) runs Tue/Fri 1pm — designed for Google Meet + tl;dv transcripts
- Does NOT cover AI Profit Boardroom calls (Fathom/Skool) which happen Mon/Thu
- Boardroom Community Monitor (7a1e3a0b5044) runs Wed only — also doesn't cover Mon/Thu calls
- **Gap**: No automated pickup of Boardroom Fathom links on call days
- **Fix needed**: Update cron to check for Fathom/Skool coaching calls on Mon/Thu, or create a separate Boardroom-specific cron
- June 16 call was missed — user had to look for it manually
