#!/usr/bin/env python3
"""
Weekly AI Profit Boardroom Community Monitor.
Uses Kimi WebBridge to scrape the Skool community feed,
extracts new posts since last run, and saves them for analysis.

Usage: python3 boardroom_monitor.py [--full]
  --full: scrape all posts (not just new ones)
"""

import subprocess, json, time, os, sys, re
from datetime import datetime

WEBADDR = "http://127.0.0.1:10086/command"
OUTPUT_DIR = "/home/tom/Desktop/coaching_call/community_scrapes"
STATE_FILE = os.path.join(OUTPUT_DIR, "last_scrape.json")

def wb(session, action, **kwargs):
    payload = {"action": action, "args": kwargs, "session": session}
    cmd = ["curl", "-s", "-X", "POST", WEBADDR,
           "-H", "Content-Type: application/json", "-d", json.dumps(payload)]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return json.loads(result.stdout)

def js(session, code):
    r = wb(session, "evaluate", code=code)
    return r.get("data", {}).get("value", "")

def nav(session, url, wait=8):
    wb(session, "navigate", url=url, newTab=False, group_title=session)
    time.sleep(wait)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_scrape": "", "seen_posts": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def extract_posts(text):
    """Extract individual posts from raw page text."""
    posts = []
    # Split by double newlines and filter
    blocks = text.split('\n\n')
    current = []
    for block in blocks:
        block = block.strip()
        if not block:
            if current:
                post_text = '\n'.join(current)
                if len(post_text) > 80:
                    posts.append(post_text)
                current = []
            continue
        # Skip navigation elements
        skip_patterns = [
            'community', 'classroom', 'calendar', 'members', 'leaderboard',
            'about', 'pinned', 'write something', 'download app', 'watch 60',
            'find a post', 'start here', 'introduce yourself', 'more...',
            '🤖 general', '? questions', '🏆 wins', '🎯 goals', '🤑 affiliate',
            '🎬 livestreams', 'intro 👋', 'weekly updates', 'changelog',
            'all\n', 'welcome! start here'
        ]
        if any(p in block.lower() for p in skip_patterns) and len(block) < 120:
            continue
        current.append(block)
    if current:
        post_text = '\n'.join(current)
        if len(post_text) > 80:
            posts.append(post_text)
    return posts

def is_useful(post):
    """Check if a post contains actionable intelligence."""
    keywords = [
        "tool", "agent", "automat", "workflow", "seo", "memory", "blog",
        "scrape", "claude", "codex", "gemini", "chatgpt", "openai",
        "supabase", "lovable", "replit", "bolt", "cursor", "n8n", "zapier",
        "api", "mcp", "rag", "vector", "ranking", "local seo", "google maps",
        "content", "pipeline", "revenue", "client", "scale", "automation",
        "hermes", "obsidian", "agent os", "heygen", "avatar", "lead gen",
        "gohighlevel", "ghl", "email", "marketing", "funnel", "conversion"
    ]
    post_lower = post.lower()
    score = sum(1 for kw in keywords if kw in post_lower)
    return score >= 2

def main():
    full_mode = "--full" in sys.argv
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    state = load_state()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    print(f"=== AI Profit Boardroom Monitor ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'FULL' if full_mode else 'INCREMENTAL'}")
    print()
    
    # Navigate to community
    print("[1/4] Loading community feed...")
    nav("monitor", "https://www.skool.com/ai-profit-lab-7462", wait=10)
    
    # Scroll to load more posts
    print("[2/4] Scrolling for content...")
    for i in range(8):
        js("monitor", "window.scrollBy(0, 3000)")
        time.sleep(2)
    
    # Extract content
    print("[3/4] Extracting posts...")
    raw_text = js("monitor", "document.body.innerText")
    
    # Save raw feed
    with open(f"{OUTPUT_DIR}/raw_feed_{timestamp}.txt", "w") as f:
        f.write(raw_text)
    
    posts = extract_posts(raw_text)
    print(f"  Total posts extracted: {len(posts)}")
    
    # Filter for useful posts
    useful = [p for p in posts if is_useful(p)]
    print(f"  Useful posts: {len(useful)}")
    
    # Filter for new posts (not seen before)
    seen = set(state.get("seen_posts", []))
    new_posts = []
    for post in useful:
        # Use first 100 chars as fingerprint
        fp = post[:100].strip()
        if fp not in seen or full_mode:
            new_posts.append(post)
            seen.add(fp)
    
    print(f"  New posts: {len(new_posts)}")
    
    # Save results
    output_file = f"{OUTPUT_DIR}/monitor_{timestamp}.txt"
    with open(output_file, "w") as f:
        f.write(f"AI Profit Boardroom — Community Monitor\n")
        f.write(f"Scraped: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total posts: {len(posts)} | Useful: {len(useful)} | New: {len(new_posts)}\n")
        f.write("=" * 60 + "\n\n")
        
        if new_posts:
            for i, post in enumerate(new_posts, 1):
                f.write(f"--- New Post #{i} ---\n")
                f.write(post[:1500])
                f.write("\n\n")
        else:
            f.write("No new useful posts since last scrape.\n")
    
    # Update state
    state["last_scrape"] = timestamp
    state["seen_posts"] = list(seen)[-500:]  # Keep last 500 fingerprints
    save_state(state)
    
    # Clean up
    wb("monitor", "close_session")
    
    print(f"\n[4/4] Saved: {output_file}")
    print(f"=== DONE ===")
    
    # Return new posts count for cron job
    return len(new_posts)

if __name__ == "__main__":
    count = main()
    sys.exit(0 if count >= 0 else 1)
