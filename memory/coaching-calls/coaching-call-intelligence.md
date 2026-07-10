# Coaching Call Intelligence — 2026-07-09

## Summary
Health/wellness tangent (aloe vera, potassium, lead, Roman Empire) → shifted to AI agent workflows. Main topics: multi-agent orchestration, human-as-validator, context window hygiene, CLI vs. desktop for multi-project workflows.

---

## Key Topics + Determinations

### 1. Multi-Agent Orchestration (Claude Fable Build)
**What they said:**
- Using 13-15 agents collaborating via an orchestrator
- Orchestrator reviews yesterday's work at 4:30 AM, assigns today's tasks
- Agents work in background, deliver finished output

**Determination:** ✅ **High value for us.**
- We can implement this via `delegate_task` (Hermes already has this)
- **Action:** Build "Goal Mode" loop (orchestrator → leaf agents → validate → retry)
- **Why useful:** Tom has 20 projects, gets bottlenecked waiting for agents. Letting them run in background + validate at end solves this.

---

### 2. Human as Validator (Not Bottleneck)
**What they said:**
> *"The ability to differentiate between being a bottleneck and a validator is going to be one of the most important skills."*

**Determination:** ✅ **Critical mindset shift for Tom.**
- Don't validate every 30s — let agents run, validate at end
- **Action:** Implement `delegate_task` with `max_iterations=5` + grading rubric
- **Why useful:** Tom's ADHD + 20 projects = constant context switching. Letting agents run frees him to focus.

---

### 3. Morning Briefing (Auto-Generated)
**What they said:**
- Orchestrator agent delivers morning brief at wake-up
- Brief includes: yesterday's progress, today's assigned tasks

**Determination:** ✅ **Already partially implemented.**
- Tom has `Atlas Daily Morning Briefing` cron (7 AM)
- **Action:** Enhance it to pull from `todo` list + memory, assign tasks for the day
- **Why useful:** Wakes up to a plan, no decision fatigue.

---

### 4. End-of-Day Sync (Context Window Hygiene)
**What they said:**
- Claude summarizes work, updates Obsidian, commits to GitHub, saves to memory
- Then clears context (`/clear`) to avoid bloat

**Determination:** ✅ **Already implemented, needs minor tweak.**
- Tom has `Hermes Chats → Obsidian Auto-Save` cron (10 PM)
- **Action:** Add "auto-summarize + clear context" step to the cron
- **Why useful:** Prevents context window bloat, keeps memory clean.

---

### 5. CLI + Browser Tabs > Claude Desktop (for Multi-Project)
**What they said:**
- Claude Desktop is great for single projects, but clunky for 5-10 concurrent ones
- Power users prefer CLI + browser tabs (instant switching)

**Determination:** ✅ **Validates Tom's current workflow.**
- Tom uses Hermes via Telegram + terminal (essentially CLI)
- **Action:** None — keep doing what he's doing
- **Why useful:** Confirmation that his workflow is optimal for his ADHD + multi-project style.

---

### 6. Model Routing (Claude Code + Multiple Models)
**What they said:**
- Building routing into Claude Code to use different models for different tasks
- Reduces waste, improves quality

**Determination:** ⚠️ **Interesting but low priority.**
- Hermes already has MoA (Mixture of Agents) — similar concept
- **Action:** Research Claude Code's routing implementation, see if we can adapt
- **Why useful:** Could optimize token usage + output quality.

---

### 7. Chinese Models (Model Data Risk)
**What they said:**
- Lot of Chinese models have data risk concerns
- Need model data risk assessment

**Determination:** ❌ **Not relevant for us (we use open-source + trusted APIs).**
- Tom uses open-source (Qwen3, etc.) + OpenRouter (trusted providers)
- **Action:** Skip — no need to assess models we're not using.

---

## Tools/Workflows Mentioned

| Tool/Workflow | Mentioned By | Useful for Us? | Action |
|----------------|---------------|-----------------|--------|
| **Claude Fable (multi-agent)** | Call participant | ✅ Yes | Implement via `delegate_task` |
| **Morning brief (auto)** | Call participant | ✅ Yes | Enhance existing cron |
| **End-of-day sync** | Call participant | ✅ Yes | Add to existing cron |
| **Claude Code routing** | Call participant | ⚠️ Maybe | Research later |
| **Obsidian integration** | Call participant | ✅ Yes | Already implemented |
| **GitHub auto-commit** | Call participant | ✅ Yes | Add to end-of-day cron |

---

## Actionable Recommendations (Prioritized)

| Priority | Action | Time Estimate |
|----------|--------|---------------|
| **1** | Implement Goal Mode loop (`delegate_task` + grading rubric) | 2-3 hours |
| **2** | Enhance Morning Briefing cron (pull from `todo` + memory) | 1 hour |
| **3** | Add end-of-day summary + context clear to existing cron | 1 hour |
| **4** | Research Claude Code routing (for future optimization) | 30 min research |

---

## Deeper Research Needed

1. **Claude Fable build** — How exactly does the orchestrator assign tasks to 13-15 agents? (Need to research)
2. **Grading rubric for `delegate_task`** — What criteria to use for "success"?
3. **Claude Code routing implementation** — How to replicate in Hermes?

---

## Raw Notes (for future reference)
- Health tangent: aloe vera, potassium, magnesium, lead, Roman Empire, plumbing
- ADHD + 20 projects → need CLI + browser tabs, not desktop
- Context window hygiene: regularly compact/save state
- Validator vs. bottleneck: important future skill

---

*Generated by Atlas from coaching call transcript (2026-07-09). Raw transcript: `/home/tom/meet-record/transcripts/coaching_call_20260709.txt`*
