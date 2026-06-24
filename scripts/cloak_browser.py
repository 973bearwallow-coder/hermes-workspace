#!/usr/bin/env python3
"""CloakBrowser stealth browser wrapper.

Usage:
    from cloak_browser import stealth_browser, stealth_page
    
    browser = stealth_browser(headless=True)
    page = browser.new_page()
    page.goto("https://protected-site.com")
    print(page.title())
    browser.close()

Or use the context manager:
    with stealth_browser_ctx(headless=True) as browser:
        page = browser.new_page()
        page.goto("https://protected-site.com")
"""

import sys
import os

# Use the cloakbrowser venv's Python
CLOAK_BROWSER = "/home/tom/hermes-workspace/venvs/cloakbrowser/bin/python3"

def stealth_browser(headless=True, humanize=False, proxy=None):
    """Launch a stealth Chromium browser.
    
    Args:
        headless: Run headless (default True)
        humanize: Enable human-like mouse/keyboard (default False)
        proxy: Proxy URL string (optional)
    
    Returns:
        Playwright Browser object
    """
    from cloakbrowser import launch
    return launch(headless=headless, humanize=humanize, proxy=proxy)


def stealth_browser_ctx(headless=True, humanize=False, proxy=None):
    """Context manager for stealth browser."""
    from contextlib import contextmanager
    
    @contextmanager
    def _ctx():
        browser = stealth_browser(headless=headless, humanize=humanize, proxy=proxy)
        try:
            yield browser
        finally:
            browser.close()
    
    return _ctx()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CloakBrowser stealth browser test")
    parser.add_argument("url", nargs="?", default="https://www.google.com", help="URL to visit")
    parser.add_argument("--no-headless", action="store_true", help="Run in headed mode")
    parser.add_argument("--humanize", action="store_true", help="Enable human-like behavior")
    args = parser.parse_args()
    
    browser = stealth_browser(headless=not args.no_headless, humanize=args.humanize)
    page = browser.new_page()
    page.goto(args.url, timeout=30000)
    print(f"Title: {page.title()}")
    print(f"URL: {page.url}")
    content = page.inner_text("body")[:500]
    print(f"\nContent:\n{content}")
    browser.close()
