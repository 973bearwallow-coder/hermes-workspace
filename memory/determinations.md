# Determinations (actionable intelligence — keep forever)

> Per coaching-call retention rule: extract what actually works, not raw transcripts.
> Status: ❓ unknown · 🔄 researching · ✅ confirmed working

## Last30Days — open-source agent search engine (2026-07-16)

**What it is:** `github.com/mvanhorn/last30days-skill` — AI agent tool that searches
walled-garden platforms (Reddit, X, YouTube, TikTok, HN, Polymarket, GitHub) that
normal LLM search can't reach. GitHub Trending #1. Has native Hermes support.

**Status:** ✅ confirmed working (tested 2026-07-16)

**Free sources (zero API key, work now):**
- Reddit (keyless RSS + arctic-shift backfill)
- Hacker News (Algolia API)
- Polymarket (prediction markets)
- Jobs boards

**Locked sources (need key/cookies):**
- X/Twitter → needs xAI API key OR browser cookies (Firefox best on Linux)
- TikTok / Instagram → free ScrapeCreators key (scrapecreators.com)
- YouTube comments → yt-dlp

**Install:** symlinked into `~/.hermes/skills/research/last30days`
(source: `/home/tom/tools/last30days-skill/skills/last30days`)
Run with `python3.12 scripts/last30days.py "topic" --search=reddit,hackernews --emit=compact`
Requires Python 3.12+ (already on system at /usr/bin/python3.12).

**Real test result:** "AI agent frameworks 2026" → 12 Reddit threads (1,066 upvotes,
245 comments) + 12 HN stories (1,864 points, 1,157 comments) in 26s. No keys.

**X account plan (if needed later):** Tom has NO X account (per memory). To enable X:
1. x.com signup with 973bearwallow@gmail.com + phone verify
2. x.ai/api signup → API key → add to Last30Days .env as XAI_API_KEY
3. Reserved handle: **@TomTorok973**
Cost: pennies/query. NOT needed for current use — free sources cover 90%.

**Why it matters:** This is the "scraper that bypasses bot restrictions" Tom saw on
YouTube (Last30Days video by Matt Van Horn). Complements Bright Data (website scraping)
— Last30Days = social-platform search, Bright Data = anti-bot website scraping.

## Free-tier MoA fix (2026-07-16)

**Bug:** Free grade selected weak `tier="free"` models (deepseek-coder-6.7b) because
strong free models (hy3, deepseek-v4-flash) are catalogued as `tier="cheap"` despite
~$0.0000002/token cost.

**Fix:** `_eligible` free selection now filters by ACTUAL price (<$0.000001/token),
not the `tier` label. Free aggregator prefers hy3. Verified: Free now builds complete
pages at $0.00.

## Video pipeline fix (2026-07-16)

**Bug:** `vision_doc` task picked non-video models (mimo-v2.5) as aggregator — couldn't
see video, returned "cannot access video file."

**Fix:** `vision_doc` base filter now requires `modalities.video=True`. Correctly picks
gemini/gemini-2.5-flash (free, video-capable). Tested: Big Buck Bunny clip described
accurately, $0.00, 2893 video tokens processed.

## Coaching Call — AI Builders Guild (2026-07-16, 152 min)

**Status:** ✅ extracted → `coaching-calls/2026-07-16-ai-builders-guild.md`

### Field-validated patterns (apply to our MoA/Atlas)
- **D1 Multi-model routing by task** (Gemini=creative, Claude=writing, Codex=critical-check) — our MoA ref+aggregator already does this. ✅
- **D2 Medium-tier > max-tier** — Claude medium ≈ high quality at 2x token savings (Alex Finn tested). → Our default deepseek-v4-flash is right. ✅
- **D3 Cross-model code review** — Claude writes, Codex reviews catches blind spots. → Add "review" mode to MoA (build A, critique B). ⚠️ not built yet
- **D4 Orchestrator-delegates** — Keith: tell ONE orchestrator WHAT, it selects agents. → Validates our subagent/dispatch architecture. ✅
- **D5 Hermes finishes tasks** — repeated: Claude "gives up," Hermes "goes to end." Core differentiator we leverage. ✅
- **D6 Per-profile LLM for latency** — CyberRick's Nova: each profile = own LLM, dropdown switch. → Maps to our model-switcher. ✅

### Caution lessons
- **C1** Don't give away free — charge $250+ up front (CyberRick). If we productize.
- **C2** AgentOS analysis paralysis — keep MoA UI simple (Plan/Clone/Research only).
- **C4** Step-by-step automation, not big-bang — our incremental MoA builds were right.

### Investigate
- **R1** Hermes Cloud + Kanban pricing (~$0.30/day hibernation) — verify via web_search
- **R2** Julian Goldie AgentOS repo — compare UX to our MoA dashboard
- **R3** NotebookLM as multi-domain "galaxy" memory — informs our shared memory bridge

### Action items from call (Tom's interest)
- Create Hermes skill to audit Claude Code projects (Git status, deps) — Jeff's ask, applicable to our multi-project setup
- Build niche demo sites; $250 migration + $25-35/mo hosting pricing model (if productizing)

## Coaching Call — AI Profit Boardroom (2026-07-17, 285 min)

**Status:** ✅ extracted → `coaching-calls/2026-07-17-ai-profit-boardroom.md`

### Field-validated patterns (apply to our Atlas/MoA)
- **D1 Shared "brain" via Obsidian** — Rashad + Keith both dump ALL AI notes/files into local Obsidian, query as knowledge base, use graph view for linkages. → DIRECTLY validates our shared memory bridge (memory_bridge.py + MEMORY.md). We're ahead: programmatic subbot access vs their manual. ✅
- **D2 Auto model-routing by task** — GenSpark (Stan/Russell) auto-picks best of 50 models per task to cut cost. → Our MoA ref+aggregator does this. Validation. ✅
- **D3 Collective brain > single agent** — put files in one store, AI draws from all; mastermind synergy. → Validates Agent OS concept Tom wanted. ✅
- **D4 Hermes completes tasks (differentiator)** — Jeff: "Hermes goes to end, Claude gives up." (same as 7/16 D5) ✅
- **D5 Comet/browser AI for night research** — Keith: Hermes uses Chrome/Comet for research, dumps to browser. → We have browser_navigate + Kimi WebBridge. ✅

### Caution lessons
- **C1** Hermes loose guardrails noted (asks for API keys directly) — our .env + redaction is safer. If productizing, harden.
- **C2** Don't build me-too widgets — 10s of M vibe-coders; find blue-ocean/infrastructure (John M.).
- **C3** Auto-routing tools burn tokens (GenSpark "chews tokens") — our free-cap + cheap-default avoids.
- **C4** Trust before JV; first 10 beta → 100 paying = valley of death.

### Investigate
- **R1** GenSpark as MoA alternative — 50 models, free image/video gen. 🔄 compare UX
- **R2** Obsidian as Agent OS memory backend — we have vault at ~/Documents/ObsidianVault. ❓
- **R3** Blockchain-encrypted cross-agent file sharing (John M.). ❓
- **R4** Comet browser for Atlas night-research. ❓

### Action items (Tom's interest)
- Keep shared memory bridge as core (DONE — already built)
- AI Builders Guild (Rick's, 65+ members) = mastermind for joint builds; Fathom archived w/ clickable transcript

## Coaching Call — Coaching Calls (2026-08-31, 182 min)

**Status:** ✅ Fathom recap extracted → `coaching-digests/2026-08-31-coaching-calls.md`

### Apply now
- **D1 Strategy before execution:** define goals, architecture, constraints, acceptance criteria, and tests in a strategic planning pass before handing implementation to a coding agent. This directly validates the Atlas (strategy) → Charles (execution) split. ✅
- **D2 Independent code audit:** AI-generated code should receive a second-agent review for dead code, security, regressions, and requirement coverage. ✅
- **D3 Sustained-use economics:** avoid metered builder credits for production when a local or predictable subscription path exists; the recap cited roughly $7 per build after included credits. ✅

### Investigate before adoption
- **R1 “GrokBot VPS”:** the call attributed an 8-CPU/16-GB remote environment and large cost savings to this name, but an exact-product public search returned no corroborating source. Confirm identity, terms, privacy, persistence, and true sustained cost before testing; use only synthetic/public data initially. 🔄

### Product pattern, not a commitment
- A mobile field companion using photo/voice notes, GPS, job records, and export may fit Paw Prints eventually, but only after mapping the actual workflow and confirming the business need. ❓

### Tom-specific assignments
- None identified in the Fathom recap.

## Coaching Call — AI Profit Boardroom (2026-06-30, reviewed 2026-09-01)

**Status:** ✅ full transcript reviewed with sampled visual evidence → `/home/tom/meet-record/summaries/2026-06-30-ai-profit-boardroom.md`

### Adopted operational patterns
- **D1 Evidence-focused call review:** use timestamped transcript cues to create small before/at/after keyframe clusters and a manifest. A visible interface proves only that an interface existed, not that the claimed outcome worked. ✅ implemented in `scripts/extract_screenshots_on_share.py`
- **D2 Structured handoffs:** before compaction or transfer, record objective, acceptance criteria, completed/current/remaining state, blockers, changed files, actual test results, exact next action, external read-back, and rollback/checkpoint state. ✅ implemented in `templates/handover-md-template.md`
- **D3 Project isolation and Git awareness:** inspect repository status before and after work; preserve unrelated dirty files and record checkpoints rather than assuming chat context is durable. ✅

### Explicit non-adoptions
- **C1 Autonomous LinkedIn commenting:** ❌ do not implement. The demo showed active debugging, not reliable conversion; account-policy and reputation risk outweigh the evidence. Human-reviewed drafting remains acceptable.
- **C2 Bulk “Agency” agent import:** ❌ do not install wholesale. Unverified scale claims do not justify role overlap, prompt bloat, or importing untrusted code; evaluate individual roles only against a concrete gap.
- **C3 Claude-centered migration:** ❌ do not migrate Atlas/Hermes. The useful patterns already fit Hermes without tying core operations to a quota-limited vendor.
- **C4 Pinterest automation:** ⚠️ no autonomous system. Consider only a bounded, manual, human-reviewed experiment when Paw Prints has a specific evergreen visual campaign and success metric.

### Tom-specific assignments
- None identified.

## MoA can build WORKING Flask apps from prompt (2026-07-16)

**Test:** Recipe Recommendation Dashboard prompt (recipe-vault/MOA_RECIPE_DASHBOARD_PROMPT.md)
run via MoA Free tier. Result: 252-line Flask app, 9KB, generated in ~16s.

**Verdict: ✅ PASSED** — not just websites, real apps with logic.
- Cuisine cleanup worked (stripped `| type:` suffixes, excluded non-cuisine words)
- NL search + ingredient-index matching worked ("Asian broccoli" → thai/chinese recipes)
- Makeable-now badge + match % present
- Launched on :8780, title "Recipe Dashboard"

**ONLY gap:** Environment. MoA ran under system `python3` (no Flask).
Fix: launch with `/home/tom/.hermes/hermes-agent/venv/bin/python3` OR add
Flask auto-install to generated script. Prompt patched to include shebang +
`try/except ImportError: pip install flask` fallback.

**Lesson:** MoA capability > website generation. Validated for multi-file-logic apps.
Free tier (deepseek-v4-flash) sufficient for code-gen; execution env must be specified.
