# Coaching Call Intelligence — AI Builders Guild (Jul 16, 2026)

**Source:** Fathom share (152 min) — AI Profit Boardroom / AI Builders Guild community call
**Attendees:** Jeff Wurfel (host), Russell Walsh, CyberRick, Ed Grimshaw, Stuart Robertson (UK), Faizan Ashraf, Greg Maestro, S. Salim (Australia), Aaron (WeDigCode), Keith Obrosky, Henry Alouf
**Extracted by:** Atlas/Hermes

---

## Summary (2-3 sentences)
A wide-ranging community call on multi-model AI orchestration, Hermes vs Claude/Codex workflows, AgentOS (Julian Goldie), tokenomics, and client-acquisition strategy for AI website/automation businesses. Key theme: **route tasks to the right model** (Gemini=creativity, Claude=realism/writing, Codex=critical check; use medium not max to save tokens) and **build an orchestrator that delegates to sub-agents** rather than doing work yourself.

---

## Key Topics
1. **Multi-model orchestration** — connecting Gemini + Claude + Codex for one task, each handling its strength
2. **Profiles per task** — CyberRick's "Nova" uses per-profile LLM assignment (marketing/video/demo) for latency control
3. **Orchestrator pattern** — Keith: one orchestrator agent selects other agents; "tell it WHAT, not HOW"
4. **Tokenomics** — Russell's framing: it all comes down to tokens, efficiency, electricity
5. **Hermes vs Claude** — Hermes finishes tasks to completion; Claude sometimes gives up; Claude better at coaching/strategy
6. **Code review across models** — Stuart: Claude writes, Codex reviews → catches blind spots
7. **AgentOS (Julian Goldie)** — unified OS organizing Claude/Hermes/OpenClaw environments
8. **Hermes Cloud + Kanban** — spin up instances, stack tasks, walk away
9. **Client pricing** — CyberRick: charge $250 min for landing page + $25-35/mo hosting retainer; don't give away free
10. **Website cloning business** — Faizan: 1-click clone WordPress → modern Next.js, 25+ niche templates
11. **"Galaxy" knowledge system** — S. Salim: vector-brain per industry, parent/child nodes, offline voice capture

---

## Determinations (✅ confirmed / ⚠️ caution / ❓ investigate)

### ✅ CONFIRMED WORKING (for our setup)
- **D1: Multi-model routing by task type works** — Gemini (creativity) + Claude (writing/realism) + Codex/OpenAI (critical check) is a real, repeated pattern in the field. → *Our MoA already does this (ref + aggregator). Validation.*
- **D2: Medium (not max/high) reasoning saves 2x tokens, comparable quality** — Alex Finn + Elias tested: Claude medium ≈ high quality, half the tokens/time. → *Applies to our MoA: default deepseek-v4-flash (cheap) over max-tier.*
- **D3: Cross-model code review catches blind spots** — Stuart: Claude writes, Codex reviews. → *We can add a "review" step: build with one model, critique with another.*
- **D4: Orchestrator-delegates pattern scales** — Keith built site + 30-day course by telling ONE orchestrator what he wanted. → *Validates our subagent/dispatch architecture.*
- **D5: Hermes finishes tasks to completion** — repeated by multiple: Claude "gives up," Hermes "goes until the end." → *Core differentiator we already leverage.*
- **D6: Per-profile LLM assignment controls latency** — CyberRick's Nova: each profile hooked to its own LLM, dropdown switch. → *Maps to our model-switcher + skill profiles.*

### ⚠️ CAUTION / LESSONS
- **C1: Don't give away free** — CyberRick: people don't respect free; charge $250+ up front, give tangible deliverable. → *If we ever productize MoA/Paw Prints services.*
- **C2: Analysis paralysis in AgentOS** — Greg: too many shiny tools, doesn't know workflow. → *Keep our MoA UI simple: Plan / Clone / Research only.*
- **C3: AI is probabilistic, not self-aware of its own features** — Jeff: "it only has so much info." → *Don't assume MoA knows all its skills; explicit routing needed.*
- **C4: Step-by-step automation, not big-bang** — Faizan/Salim: phase departments one at a time. → *Our incremental MoA feature builds (free fix → refine → clone → video) were right approach.*

### ❓ INVESTIGATE / DEEPER RESEARCH
- **R1: Hermes Cloud + Kanban pricing** — Stuart mentioned ~$0.30/day hibernation fee, click-to-deploy. STATUS: 🔄 Need to verify current pricing/availability. (Could be alternative to our self-hosted Charles.)
- **R2: Julian Goldie AgentOS open-sourcing** — Russell built 3-4 versions past Goldie's. STATUS: ❓ Worth pulling Goldie's repo to compare with our MoA dashboard.
- **R3: NotebookLM as "galaxy" alternative** — Salim uses it for multi-industry vector brains. STATUS: ❓ Could inform our memory architecture (already have shared memory bridge).
- **R4: X/Twitter access for trend monitoring** — Last30Days needs xAI key. STATUS: ✅ Installed, free sources work; X locked pending Tom's X account.

---

## Actionable Recommendations (prioritized)

| # | Action | Why | Time est. | Priority |
|---|---|---|---|---|
| 1 | Add cross-model "review" mode to MoA (build w/ A, critique w/ B) | D3 validated in field; cheap quality lift | 2-3 hrs | High |
| 2 | Default MoA to medium-tier (deepseek-v4-flash) not max | D2: 2x token savings, same quality | 0 (already default) | Done |
| 3 | Save Last30Days as skill (not just determination) | R4: real tool, free sources work | 1 hr | Med |
| 4 | Pull Julian Goldie AgentOS repo, compare to MoA dashboard | R2: might surface UX patterns | 1-2 hrs | Low |
| 5 | Document our "orchestrator delegates" pattern as a skill | D4: we already do this; capture it | 1 hr | Med |

---

## Deeper Research Needed
- [🔄] R1: Hermes Cloud pricing + Kanban — verify via web_search
- [❓] R2: Julian Goldie AgentOS GitHub repo
- [❓] R3: NotebookLM API for multi-domain memory
- [✅] R4: Last30Days — installed + tested, X locked pending Tom's X account

---

## Raw artifacts
- Fathom share: https://fathom.video/share/SHBNEjXisrsxvemS6kSWEscUxt3gXKxP
- Transcript saved: /home/tom/.hermes/cache/documents/doc_11341800e82e_message.txt
- Retention: raw transcript + this file DELETE after 30 days (2026-08-15); determinations above → KEEP FOREVER in memory/determinations.md
