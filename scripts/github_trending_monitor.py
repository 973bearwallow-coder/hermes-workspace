#!/usr/bin/env python3
"""
GitHub Trending & Interesting Repos Monitor
Searches GitHub for trending repos using the REST API (no gh CLI needed).
Focuses on AI agents, tools, SEO, automation, local LLM, and pet business tech.
"""

import urllib.request
import urllib.parse
import json
import os
import sys
from datetime import datetime, timezone, timedelta

OUTPUT_DIR = os.path.expanduser("~/hermes-workspace/memory")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# GitHub API endpoint
GITHUB_API = "https://api.github.com"

# Search queries tailored to our interests
# Format: (category, query, min_stars)
SEARCH_QUERIES = [
    ("AI Agents & MCP", "agent mcp tool", 100),
    ("LLM Skills & Plugins", "llm plugin skill workflow", 100),
    ("SEO & Marketing Tools", "seo marketing automation local", 50),
    ("No-Code Automation", "automation workflow no-code ai", 100),
    ("Local LLM & Self-Hosted", "ollama llama.cpp local-llm", 200),
    ("Pet Business Tech", "pet dog business ecommerce", 10),
    ("Browser & Scraper Tools", "browser scraper automation python", 100),
    ("Content Pipeline", "content scraper ai summarize blog", 50),
]

def github_search(query, min_stars=50, sort="stars", per_page=10):
    """Search GitHub API for repos"""
    params = urllib.parse.urlencode({
        "q": f"{query} stars:>={min_stars}",
        "sort": sort,
        "order": "desc",
        "per_page": per_page
    })
    url = f"{GITHUB_API}/search/repositories?{params}"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Atlas-GitHub-Monitor/1.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("items", [])
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"  ⛔ Rate limited (403). Try again in 60s.")
        else:
            print(f"  HTTP error {e.code}: {e.reason}")
        return []
    except Exception as e:
        print(f"  Error: {e}")
        return []

def get_trending_recent():
    """Get repos created in last 7 days, sorted by stars"""
    EDT = timezone(timedelta(hours=-4))
    week_ago = (datetime.now(EDT) - timedelta(days=7)).strftime("%Y-%m-%d")
    return github_search(f"created:>{week_ago}", min_stars=50, per_page=15)

def score_repo(repo):
    """Score relevance to our use case"""
    score = 0
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    name = (repo.get("full_name") or "").lower()
    lang = (repo.get("language") or "").lower()
    combined = f"{desc} {' '.join(topics)} {name}"

    # High relevance
    high_kw = ["agent", "skill", "plugin", "mcp", "automation", "ai",
               "seo", "marketing", "workflow", "ollama", "llama",
               "self-hosted", "no-code", "open-source", "browser",
               "scraper", "summarize", "transcribe"]
    for kw in high_kw:
        if kw in combined:
            score += 3

    # Medium relevance
    medium_kw = ["python", "cli", "api", "tool", "productivity",
                 "local", "markdown", "database", "vector"]
    for kw in medium_kw:
        if kw in combined:
            score += 1

    # Language bonus
    if lang in ["python", "typescript", "rust", "go"]:
        score += 1

    # Stars
    stars = repo.get("stargazers_count", 0)
    if stars > 10000: score += 4
    elif stars > 5000: score += 3
    elif stars > 1000: score += 2
    elif stars > 500: score += 1

    # Recent
    updated = repo.get("updated_at", "")
    if updated:
        try:
            dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - dt).days
            if age_days < 3: score += 3
            elif age_days < 7: score += 2
            elif age_days < 30: score += 1
        except:
            pass

    return score

def main():
    EDT = timezone(timedelta(hours=-4))
    now = datetime.now(EDT)
    date_str = now.strftime("%Y-%m-%d")

    print("=" * 60)
    print("🔍 GitHub Trending & Interesting Repos Monitor")
    print(f"📅 {now.strftime('%Y-%m-%d %H:%M %Z')}")
    print("=" * 60)
    print()

    all_results = []

    # Method 1: Targeted searches
    for category, query, min_stars in SEARCH_QUERIES:
        print(f"📂 {category}...")
        repos = github_search(query, min_stars=min_stars)
        if repos:
            scored = [(score_repo(r), r) for r in repos]
            scored.sort(key=lambda x: x[0], reverse=True)
            interesting = [(s, r) for s, r in scored if s >= 4]
            if interesting:
                print(f"  ✅ {len(interesting)} interesting:")
                for score, repo in interesting[:4]:
                    s = repo.get("stargazers_count", 0)
                    d = (repo.get("description") or "")[:70]
                    print(f"  ⭐{s:,} [{score}pts] {repo['full_name']}")
                    print(f"  {d}")
                    all_results.append({
                        "category": category,
                        "repo": repo,
                        "score": score,
                    })
            else:
                print(f"  Nothing great (best: {scored[0][0]}pts)")
        else:
            print(f"  No results")
        print()

        # Method 2: Recently trending (run once)
        if category == SEARCH_QUERIES[0][0]:
            print(f"🔥 Recent Trending (last 7 days)...")
            trending = get_trending_recent()
            if trending:
                scored = [(score_repo(r), r) for r in trending]
                scored.sort(key=lambda x: x[0], reverse=True)
                for score, repo in scored[:5]:
                    s = repo.get("stargazers_count", 0)
                    d = (repo.get("description") or "")[:70]
                    print(f"  ⭐{s:,} [{score}pts] {repo['full_name']}")
                    print(f"     {d}")
                    all_results.append({
                        "category": "Recent Trending",
                        "repo": repo,
                        "score": score,
                    })
            print()

    # Deduplicate
    seen = set()
    unique = []
    for item in all_results:
        name = item["repo"]["full_name"]
        if name not in seen:
            seen.add(name)
            unique.append(item)
    unique.sort(key=lambda x: x["score"], reverse=True)

    # Write output
    output_file = f"{OUTPUT_DIR}/github_trending_{date_str}.md"
    with open(output_file, "w") as f:
        f.write(f"# GitHub Trending Report — {date_str}\n\n")
        if unique:
            f.write(f"## 🔥 Top Picks ({len(unique)} repos)\n\n")
            for item in unique[:20]:
                r = item["repo"]
                f.write(f"### {r['full_name']} ⭐{r['stargazers_count']:,} (relevance: {item['score']}/20)\n")
                f.write(f"- **Category:** {item['category']}\n")
                f.write(f"- **Description:** {r.get('description', 'N/A')}\n")
                f.write(f"- **Language:** {r.get('language', 'N/A')}\n")
                f.write(f"- **Updated:** {r.get('updated_at', 'N/A')}\n")
                f.write(f"- **Topics:** {', '.join(r.get('topics', [])[:8])}\n")
                f.write(f"- **URL:** {r['html_url']}\n\n")
        else:
            f.write("No interesting repos found today.\n")

    # Summary
    print("=" * 60)
    print(f"📁 Results: {output_file}")
    print(f"🔥 Top picks: {len(unique)}")
    if unique:
        print("\n🏆 Top 5 most relevant:")
        for item in unique[:5]:
            r = item["repo"]
            lang = r.get("language", "?")
            print(f"  • {r['full_name']} ⭐{r['stargazers_count']:,} [{lang}] (score:{item['score']})")
            print(f"    {(r.get('description') or '')[:60]}")
    print("=" * 60)

if __name__ == "__main__":
    main()
