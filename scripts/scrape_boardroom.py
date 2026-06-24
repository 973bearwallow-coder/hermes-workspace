#!/usr/bin/env python3
"""Scrape AI Profit Boardroom community posts via Kimi WebBridge."""
import subprocess, json, time, sys

WEBADDR = "http://127.0.0.1:10086/command"

def wb(session, action, **kwargs):
    payload = {"action": action, "args": kwargs, "session": session}
    cmd = ["curl", "-s", "-X", "POST", WEBADDR,
           "-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)

def js(session, code):
    r = wb(session, "evaluate", code=code)
    return r.get("data", {}).get("value", "")

def scroll_and_collect(session, max_scrolls=20):
    """Scroll down the community feed and collect all posts."""
    all_posts = []
    seen_texts = set()
    
    for i in range(max_scrolls):
        # Get all post-like elements
        posts = js(session, """
JSON.stringify(Array.from(document.querySelectorAll('[class*=post], [class*=feed], [class*=card], [class*=comment]')).map(el => ({
    text: el.innerText.trim().substring(0, 500),
    class: (el.className || '').substring(0, 50)
})).filter(x => x.text.length > 50).slice(0, 20))
""")
        
        if posts:
            try:
                items = json.loads(posts)
                for item in items:
                    text = item.get('text', '')
                    if text not in seen_texts:
                        seen_texts.add(text)
                        all_posts.append(item)
            except:
                pass
        
        # Scroll down
        js(session, "window.scrollBy(0, 800)")
        time.sleep(2)
    
    # Scroll back to top
    js(session, "window.scrollTo(0, 0)")
    
    return all_posts

if __name__ == "__main__":
    session = "boardroom-scrape"
    
    # Navigate to community
    print("Navigating to community...")
    wb(session, "navigate", url="https://www.skool.com/ai-profit-lab-7462", newTab=True, group_title="scrape")
    time.sleep(5)
    
    # Click on Community tab
    result = js(session, "document.querySelector('[class*=community]') ? 'found' : 'not found'")
    print(f"Community tab: {result}")
    
    # Scroll and collect posts
    print("Scrolling and collecting posts...")
    posts = scroll_and_collection(session, max_scrolls=15)
    
    print(f"\\nCollected {len(posts)} posts")
    
    # Save to file
    with open('/home/tom/hermes-workspace/memory/boardroom_scrape.json', 'w') as f:
        json.dump(posts, f, indent=2)
    
    print("Saved to boardroom_scrape.json")
