import asyncio
import sys
sys.path.insert(0, '.')
from pet_community_monitor import ddgs_search

async def test():
    results = await ddgs_search("site:reddit.com r/doggrooming business tips", max_results=5)
    print(f"Found {len(results)} results")
    for i, r in enumerate(results, 1):
        print(f"{i}. Title: {r['title']}")
        print(f"   URL: {r['href']}")
        print(f"   Snippet: {r['body'][:100]}")
        print()

asyncio.run(test())
