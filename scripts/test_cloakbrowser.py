#!/usr/bin/env python3
"""Test CloakBrowser against various bot detection systems."""
import sys
import time

from cloakbrowser import launch

def test_site(name, url, check_fn=None):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print('='*60)
    
    browser = launch(headless=True)
    page = browser.new_page()
    
    try:
        page.goto(url, timeout=30000)
        time.sleep(3)  # Wait for JS to execute
        
        title = page.title()
        print(f"Page title: {title}")
        
        if check_fn:
            result = check_fn(page)
            print(f"Check result: {result}")
        
        # Get page content snippet
        content = page.inner_text('body')[:500]
        print(f"Content preview:\n{content[:300]}...")
        
        print(f"✅ {name} — PASSED (page loaded)")
        return True
    except Exception as e:
        print(f"❌ {name} — FAILED: {e}")
        return False
    finally:
        browser.close()

# Test 1: Basic site
test_site("Google", "https://www.google.com")

# Test 2: Cloudflare-protected site
test_site("Cloudflare", "https://www.cloudflare.com")

# Test 3: Bot detection test site
test_site("Bot Detection Test", "https://bot.incolumitas.com")

print("\n" + "="*60)
print("All tests complete!")
print("="*60)
