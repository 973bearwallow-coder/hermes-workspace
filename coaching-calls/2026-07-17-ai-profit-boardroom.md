# Coaching Call Intelligence — AI Profit Boardroom (Jul 17, 2026)

**Source:** Fathom recording (285 min) — AI Profit Boardroom community call
**Fathom call ID:** 749586922
**Fathom share:** https://fathom.video/share/AFCx8qo2T9De7M94edMjH2t9zuXQzkCh
**Transcript:** /home/tom/.hermes/cache/documents/doc_628ea697edcc_message.txt
**Attendees:** Jeff Wurfel (host), CyberRick, Keith Obrosky, John Mackenzie, Russell Walsh, Stan Barrett, Elias Siqueira, Rashad Khan, Jobi Armstrong, Ryan Gorman, TRP LLC / Tony, Aaron (WeDigCode), and others
**Extracted by:** Atlas/Hermes

---

## Summary (2-3 sentences)
A 285-minute wide-ranging call covering AI agent guardrails (Hermes vs Claude on API-key handling), the China/US AI competition, crypto/blockchain as a business model, SaaS valuation math (MRR→ARR multiples), and — most relevant to us — a deep dive on **collective "AI brain" / shared knowledge base architecture** using Obsidian + Recall + GenSpark, with the AI Builders Guild (Rick's group) positioned as the mastermind where these get built. Key actionable theme for Atlas: **build a unified shared memory "brain" (Obsidian-backed) that multiple agents query** — which validates our existing shared memory bridge.

---

## Key Topics
1. **Hermes guardrails vs Claude** — Hermes asked for API keys directly; Claude refuses. Community noted Hermes guardrails looser. (Jeff, CyberRick, Keith)
2. **China AI dominance** — China graduates more engineers/year than US has total; open-source models (Agnes) trained for Hermes tasks; data-to-China risk for IP. (Elias, Jeff, John M.)
3. **Crypto/blockchain as rails** — XRP vs SWIFT, Bitcoin as hard-money hedge, token correlations, "build on blockchain with AI" question. (Stan, Russell, Elias, John M.)
4. **SaaS valuation math** — MRR×12=ARR; angel/series multiples 10–15× ARR; traditional biz 1–4× profit. Path to monetization via community + revenue split. (John M., Stan)
5. **Obsidian as collective "brain"** — Rashad + Keith: dump all AI notes/files into Obsidian (local, free, graph view), query as knowledge base. Recall does same with web clipper. (KEY for us)
6. **GenSpark** — Stan/Russell: 50 models, auto-routes best model per task, unlimited image/video gen, $200/mo, token-heavy. Alternative to our MoA routing concept.
7. **Comet browser** — Keith: AI browser, highlight-to-summarize/fact-check, schedules tasks, Hermes uses it for night research. (Maps to our browser tooling)
8. **AI Builders Guild** — Rick's group (65+ members), compliments this call; Fathom recordings archived with clickable transcript; mastermind for building joint projects.
9. **"Stop building widgets, build infrastructure"** — John M./Keith: think AWS/Cloudflare-level rails, not me-too SaaS. Blockchain for encrypted file-sharing across untrusted networks.
10. **GoHighLevel + bots** — Stan/Russell: GHL's Ask AI (7 bot types), outbound call bots, connect any LLM via API/Zapier.

---

## Determinations (✅ confirmed / ⚠️ caution / ❓ investigate)

### ✅ CONFIRMED WORKING (for our setup)
- **D1: Shared-memory "brain" via Obsidian is field-validated** — Rashad + Keith both run ALL AI notes/files into local Obsidian, query it as a knowledge base, use graph view to find linkages. → *DIRECTLY validates our shared memory bridge (memory_bridge.py + MEMORY.md). Our architecture is ahead — we have programmatic subbot access; Obsidian is their manual equivalent.*
- **D2: Auto model-routing by task saves tokens** — GenSpark (Stan/Russell) auto-picks best of 50 models per task to cut cost. → *Our MoA ref+aggregator does exactly this. Validation.*
- **D3: "Collective brain" > single agent** — repeated: put files in one VPS/storage, AI draws from all; mastermind synergy. → *Validates Agent OS concept Tom asked for. Our subbot memory bridge is the implementation.*
- **D4: Hermes completes tasks (differentiator)** — Jeff: "Hermes goes to the end, Claude gives up." → *We already leverage this (D5 from 7/16 call).*
- **D5: Comet/browser AI for research** — Keith: Hermes uses Chrome/Comet for night research, dumps to browser. → *We have browser_navigate + Kimi WebBridge; comparable.*

### ⚠️ CAUTION / LESSONS
- **C1: Loose guardrails on Hermes noted by users** — community flagged Hermes asking for API keys directly. → *We already redact keys + use .env; our setup is safer than default Hermes. Note for any productized service.*
- **C2: Don't build me-too widgets** — John M.: 10s of millions of vibe-coders building same tools; find blue-ocean/infrastructure. → *Applies if we productize MoA/Paw Prints.*
- **C3: Token burn with auto-routing tools** — Stan: GenSpark "will chew your tokens, beat you up." → *Our MoA free-tier cap + cheap-default (deepseek-v4-flash) avoids this.*
- **C4: Trust before JV** — Stan/John M.: find people you like+trust before building; first 10 beta → 100 paying = valley of death. → *If joint-building in Guild.*

### ❓ INVESTIGATE / DEEPER RESEARCH
- **R1: GenSpark as MoA alternative** — 50 models, auto-route, free image/video. STATUS: 🔄 Compare to our MoA dashboard; may inform routing UX.
- **R2: Obsidian as our memory backend** — Rashad/Keith use it as queryable brain. STATUS: ❓ We use flat MEMORY.md + memory_bridge.py; Obsidian graph could supplement. (We already have Obsidian vault at ~/Documents/ObsidianVault.)
- **R3: Blockchain-encrypted file sharing** — John M.: encrypt files on blockchain, share across untrusted nets without AWS. STATUS: ❓ Interesting for Agent OS security; research lightweight impl.
- **R4: Comet browser for Atlas night-research** — Keith uses it; we have browser_navigate. STATUS: ❓ Could adopt Comet if beneficial.

---

## Actionable Recommendations (prioritized)

| # | Action | Why | Time est. | Priority |
|---|---|---|---|---|
| 1 | Keep shared memory bridge as core (already built) | D1/D3: field-validated collective brain concept | 0 (done) | Done |
| 2 | Save GenSpark comparison as research note | R1: potential MoA UX lessons | 1 hr | Low |
| 3 | Test Obsidian graph as memory supplement | R2: we have vault already; low effort | 1-2 hrs | Low |
| 4 | Document "stop building widgets" rule if productizing | C2: avoids me-too trap | 0 (note only) | Med |

---

## Deeper Research Needed
- [🔄] R1: GenSpark vs MoA dashboard — feature comparison
- [❓] R2: Obsidian as Agent OS memory backend (we have vault at ~/Documents/ObsidianVault)
- [❓] R3: Blockchain-encrypted cross-agent file sharing
- [❓] R4: Comet browser adoption for Atlas

---

## Raw artifacts
- Fathom call: https://fathom.video/calls/749586922 (requires login — not downloaded)
- Fathom share: https://fathom.video/share/AFCx8qo2T9De7M94edMjH2t9zuXQzkCh
- Transcript saved: /home/tom/.hermes/cache/documents/doc_628ea697edcc_message.txt
- Retention: raw transcript + this file DELETE after 30 days (2026-08-16); determinations above → KEEP FOREVER in memory/determinations.md
