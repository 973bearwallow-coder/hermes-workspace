#!/usr/bin/env python3
"""
Pet Community Intelligence Monitor.
Uses crawlee to scrape DuckDuckGo lite for relevant content across Reddit, forums, and blogs.
Focuses on: pet business tips, Etsy selling, dog groomer advice, local pet business marketing.

No API keys needed — uses crawlee to fetch and parse DuckDuckGo lite results.
"""

import json, os, sys, re
from datetime import datetime
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = "/home/tom/Desktop/coaching_call/pet_community"
STATE_FILE = os.path.join(OUTPUT_DIR, "seen_urls.json")

# Search queries targeting pet business intelligence
SEARCH_QUERIES = [
    "site:reddit.com r/doggrooming business tips pricing",
    "site:reddit.com r/EtsySellers pet products marketing",
    "site:reddit.com r/pets business ideas 2025 2026",
    "site:reddit.com r/smallbusiness dog grooming local marketing",
    "dog grooming business tips revenue pricing strategy",
    "custom pet products Etsy print on demand success",
    "local pet business SEO marketing 2025",
    "dog lover community buying habits trends",
    "pet industry trends 2025 2026 small business",
    "paw print merchandise custom printing business",
]

KEYWORDS = [
    "revenue", "profit", "sales", "marketing", "customer", "pricing",
    "etsy", "shopify", "website", "seo", "local", "advertising",
    "product", "design", "custom", "merchandise", "print", "pricing",
    "strategy", "tips", "advice", "recommend", "tool", "software",
    "workflow", "automate", "scale", "grow", "client", "booking"
]

def ddgs_search(query: str, max_results: int = 10):
    """Fetch and parse DuckDuckGo Lite without a browser dependency."""
    url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; AtlasPetMonitor/1.0)"},
        timeout=30,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for link_tag in soup.find_all("a", class_="result-link"):
        if len(results) >= max_results:
            break
        link_tr = link_tag.find_parent("tr")
        snippet_tr = link_tr.find_next_sibling("tr") if link_tr else None
        snippet_td = snippet_tr.find("td", class_="result-snippet") if snippet_tr else None
        href = link_tag.get("href", "")
        if not href:
            continue
        results.append({
            "title": link_tag.get_text(strip=True),
            "href": href,
            "body": snippet_td.get_text(strip=True) if snippet_td else "",
            "display_url": "",
        })
    return results
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_urls": [], "last_run": ""}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def score_result(result):
    """Score a search result for relevance."""
    text = (result.get("title", "") + " " + result.get("body", "")).lower()
    score = sum(1 for kw in KEYWORDS if kw in text)
    return score

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    state = load_state()
    seen = set(state.get("seen_urls", []))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    print(f"=== Pet Community Monitor ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Queries: {len(SEARCH_QUERIES)}")
    print(f"Seen URLs: {len(seen)}")
    print()
    
    all_results = []
    new_results = []
    
    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"[{i}/{len(SEARCH_QUERIES)}] Searching: {query[:60]}...")
        results = ddgs_search(query, max_results=8)
        
        for r in results:
            url = r.get("href", "")
            if url in seen:
                continue
            
            score = score_result(r)
            r["_score"] = score
            r["_query"] = query
            
            if score >= 2:
                new_results.append(r)
            
            seen.add(url)
            all_results.append(r)
        
        print(f"  Found: {len(results)} | New relevant: {len([r for r in results if r.get('_score',0) >= 2])}")
    
    # Sort by relevance
    new_results.sort(key=lambda x: x.get("_score", 0), reverse=True)
    
    # Save
    output_file = f"{OUTPUT_DIR}/intelligence_{timestamp}.txt"
    with open(output_file, "w") as f:
        f.write(f"Pet Community Intelligence Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Searches: {len(SEARCH_QUERIES)} | Results: {len(all_results)} | New relevant: {len(new_results)}\n")
        f.write("=" * 60 + "\n\n")
        
        if new_results:
            f.write(f"TOP FINDINGS ({len(new_results)} relevant results):\n\n")
            for i, r in enumerate(new_results[:30], 1):
                f.write(f"--- #{i} (score: {r['_score']}) ---\n")
                f.write(f"Title: {r.get('title', '?')}\n")
                f.write(f"URL: {r.get('href', '?')}\n")
                f.write(f"Source: {r.get('query', '?')}\n")
                body = r.get("body", "")[:800]
                f.write(f"Preview: {body}\n\n")
        else:
            f.write("No new relevant results this run.\n")
    
    # Also save raw JSON
    json_file = f"{OUTPUT_DIR}/intelligence_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "total_searches": len(SEARCH_QUERIES),
            "total_results": len(all_results),
            "new_relevant": len(new_results),
            "top_results": new_results[:30]
        }, f, indent=2)
    
    # Update state
    state["seen_urls"] = list(seen)[-2000:]
    state["last_run"] = timestamp
    save_state(state)
    
    print(f"\n=== Summary ===")
    print(f"Total results: {len(all_results)}")
    print(f"New relevant: {len(new_results)}")
    print(f"Saved: {output_file}")
    print(f"=== DONE ===")
    
    return len(new_results)

if __name__ == "__main__":
    count = main()
    sys.exit(0)