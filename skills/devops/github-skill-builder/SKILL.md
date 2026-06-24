---
name: github-skill-builder
description: >
  Monitors GitHub for interesting repos/tools and builds sanitized Hermes skills from them.
  Trigger: "check github trending", "find new AI tools", "monitor GitHub for skills".
triggers:
  - check github trending
  - find new AI tools
  - github monitor
  - new repos to check
  - build skill from repo

steps:
  - Step 1: Run trending monitor
  - Step 2: Score and filter repos
  - Step 3: Deep-dive top picks
  - Step 4: Summarize for Tom

---

# GitHub Skill Builder

## Overview
Automated pipeline to discover, evaluate, and adapt GitHub repos into Hermes-compatible skills.
Runs daily via cron, plus on-demand when Tom asks.

## Architecture

```
Daily Cron (8am)
  → github_trending_monitor.py (search + score)
  → Sub-agent evaluates top 5 picks
  → Telegram summary to Tom
  → Interesting repos → quarantine for skill building
```

## Step 1: Run the Monitor

```bash
python3 /home/tom/hermes-workspace/scripts/github_trending_monitor.py
```

Output: `~/hermes-workspace/memory/github_trending_YYYY-MM-DD.md`

## Step 2: Evaluate Results

For each top-scoring repo, check:
1. **Language** — Python/TS preferred, skip Java-heavy projects
2. **License** — Must be MIT/Apache/BSD (no GPL for business use)
3. **Complexity** — Can we extract value without the whole codebase?
4. **Relevance** — Does it solve a problem we actually have?
5. **Security** — No telemetry, no phone-home, no crypto

## Step 3: Skill Building Pipeline (for approved repos)

When Tom approves a repo for skill building:

1. **Clone to quarantine:**
   ```bash
   git clone <repo_url> /home/tom/hermes-workspace/skills/quarantine/<name>/
   ```

2. **Security review:**
   - Scan for network calls in source
   - Remove telemetry/analytics
   - Remove unnecessary dependencies
   - Check for credential access patterns

3. **Extract core functionality:**
   - Identify the useful subset (often 10-20% of the code)
   - Rewrite as a minimal Hermes skill
   - Follow skill format: SKILL.md + scripts/ + references/

4. **Install to approved:**
   ```bash
   mv /home/tom/hermes-workspace/skills/quarantine/<name>/
      /home/tom/hermes-workspace/skills/approved/<name>/
   ```

5. **Register with Hermes:**
   - Skill auto-loads via SKILL.md frontmatter
   - Test with a sample invocation
   - Document in `~/hermes-workspace/memory/skill_registry.md`

## Scoring Criteria

Score each repo 0-20 points:

| Factor | Points | Criteria |
|--------|--------|----------|
| Keyword match | +3 each | agent, skill, plugin, mcp, automation, ai, seo, workflow, ollama |
| Medium keyword | +1 each | python, cli, api, tool, productivity, local |
| Stars | +1 to +4 | 500→+1, 1k→+2, 5k→+3, 10k→+4 |
| Recent update | +1 to +3 | 30d→+1, 7d→+2, 3d→+3 |
| Language bonus | +1 | Python, TypeScript, Rust, Go |

Threshold: ≥ 4 points = "interesting", ≥ 10 = "investigate", ≥ 15 = "build skill"

## Categories Monitored

1. **AI Agents & MCP** — agent frameworks, MCP servers, tool calling
2. **LLM Skills & Plugins** — prompt engineering, skill libraries, plugin systems
3. **SEO & Marketing Tools** — local SEO, review management, GBP optimization
4. **No-Code Automation** — workflow engines, AI automation, Zapier alternatives
5. **Local LLM & Self-Hosted** — Ollama tools, llama.cpp wrappers, local inference
6. **Pet Business Tech** — niche: dog/pet business software, ecommerce
7. **Browser & Scraper Tools** — AI-powered scrapers, browser automation
8. **Content Pipeline** — scraping → AI → publish workflows
9. **Recent Trending** — repos created in last 7 days with 50+ stars

## Files

- Script: `/home/tom/hermes-workspace/scripts/github_trending_monitor.py`
- Output: `~/hermes-workspace/memory/github_trending_YYYY-MM-DD.md`
- Quarantine: `/home/tom/hermes-workspace/skills/quarantine/`
- Approved: `/home/tom/hermes-workspace/skills/approved/`

## Security Notes

- NEVER directly execute code from a cloned repo
- ALWAYS review before moving from quarantine → approved
- Strip all network calls except the core API interactions
- No external analytics, tracking, or telemetry
- Prefer pure-Python implementations over shell execs
