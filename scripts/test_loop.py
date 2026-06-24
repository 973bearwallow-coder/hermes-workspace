import asyncio
import sys
sys.path.insert(0, '.')
from pet_community_monitor import ddgs_search

async def test_all():
    for i in range(3):
        print(f"Query {i}")
        results = await ddgs_search("test", max_results=2)
        print(f"  got {len(results)} results")
        await asyncio.sleep(1)

asyncio.run(test_all())
