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
