#!/usr/bin/env python3
"""
Pet Community Intelligence Monitor.
Uses crawlee to scrape DuckDuckGo lite for relevant content across Reddit, forums, and blogs.
Focuses on: pet business tips, Etsy selling, dog groomer advice, local pet business marketing.

No API keys needed — uses crawlee to fetch and parse DuckDuckGo lite results.
"""

import asyncio, json, os, sys, re
from datetime import datetime
from bs4 import BeautifulSoup
from crawlee.crawlers import PlaywrightCrawler
from crawlee.browsers import BrowserPool, PlaywrightBrowserController
from crawlee.browsers import PlaywrightBrowserPlugin
from crawlee.browsers import PlaywrightBrowserController as PlaywrightBrowserControllerBase
from typing_extensions import override

# We'll create a simple browser plugin that uses the default Playwright Chromium
# (since we don't need CloakBrowser for this simple task)
class DefaultBrowserPlugin(PlaywrightBrowserPlugin):
    @override
    async def new_browser(self) -> PlaywrightBrowserController:
        if not self._playwright:
            raise RuntimeError('Playwright browser plugin is not initialized.')
        return PlaywrightBrowserController(
            browser=await self._playwright.chromium.launch(),
            max_open_pages_per_browser=1,
        )

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

async def ddgs_search(query: str, max_results: int = 10):
    """Search using crawlee to scrape DuckDuckGo lite."""
    url = f"https://lite.duckduckgo.com/lite/?q={query}"
    results = []

    # We'll use a crawler that just visits the URL and extracts the results
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=1,
        browser_pool=BrowserPool(plugins=[DefaultBrowserPlugin()]),
    )

    @crawler.router.default_handler
    async def request_handler(context):
        nonlocal results
        page = context.page
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        # Find all result links
        link_tags = soup.find_all('a', class_='result-link')
        for link_tag in link_tags:
            if len(results) >= max_results:
                break
            title = link_tag.get_text(strip=True)
            href = link_tag.get('href', '')
            # Find the parent <tr> of the link
            link_tr = link_tag.find_parent('tr')
            if not link_tr:
                continue
            # Snippet is in the next <tr> that has a td with class 'result-snippet'
            snippet_tr = link_tr.find_next_sibling('tr')
            snippet = ''
            if snippet_tr:
                snippet_td = snippet_tr.find('td', class_='result-snippet')
                if snippet_td:
                    snippet = snippet_td.get_text(strip=True)
            # URL is in the next <tr> after snippet that has a td with class 'link-text'
            url_tr = snippet_tr.find_next_sibling('tr') if snippet_tr else None
            display_url = ''
            if url_tr:
                url_td = url_tr.find('td', class_='link-text')
                if url_td:
                    url_span = url_td.find('span', class_='link-text')
                    if url_span:
                        display_url = url_span.get_text(strip=True)
            # Build result dict
            results.append({
                'title': title,
                'href': href,
                'body': snippet,
                # optionally store display_url if needed
                'display_url': display_url,
            })
        # We don't want to enqueue links

    await crawler.run([url])
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
        # Run the async search function
        results = asyncio.run(ddgs_search(query, max_results=8))
        
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