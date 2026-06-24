import asyncio
from crawlee.crawlers import PlaywrightCrawler
from crawlee.browsers import BrowserPool, PlaywrightBrowserPlugin
from crawlee.browsers import PlaywrightBrowserController
from typing_extensions import override

class DefaultBrowserPlugin(PlaywrightBrowserPlugin):
    @override
    async def new_browser(self) -> PlaywrightBrowserController:
        if not self._playwright:
            raise RuntimeError('Playwright browser plugin is not initialized.')
        return PlaywrightBrowserController(
            browser=await self._playwright.chromium.launch(),
            max_open_pages_per_browser=1,
        )

async def fetch():
    crawler = PlaywrightCrawler(
        max_requests_per_crawl=1,
        browser_pool=BrowserPool(plugins=[DefaultBrowserPlugin()]),
    )
    results = []
    @crawler.router.default_handler
    async def handler(context):
        page = context.page
        content = await page.content()
        # Save to file for inspection
        with open('/tmp/ddg_lite.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Saved page to /tmp/ddg_lite.html')
        # Also print title
        title = await page.title()
        print(f'Title: {title}')
    await crawler.run(['https://lite.duckduckgo.com/lite/?q=test'])
asyncio.run(fetch())
