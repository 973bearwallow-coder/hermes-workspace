import subprocess, json, time, sys, os

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

def nav(session, url, wait=7):
    wb(session, "navigate", url=url, newTab=False, group_title=session)
    time.sleep(wait)

def get_posts(session, max_scrolls=10):
    """Extract community posts from Skool feed."""
    posts = []
    
    # Get initial content
    content = js(session, """
    (function(){
        const posts = document.querySelectorAll('[class*="post"], [class*="feed-item"], [class*="card"]');
        const result = [];
        posts.forEach(function(p){
            const text = p.innerText.trim();
            if(text.length > 50){
                result.push(text.substring(0, 500));
            }
        });
        return JSON.stringify(result);
    })()
    """)
    
    if isinstance(content, str):
        try:
            posts = json.loads(content)
        except:
            pass
    
    # Scroll and get more
    for i in range(max_scrolls):
        js(session, "window.scrollBy(0, 2000)")
        time.sleep(2)
    
    # Get full page text as fallback
    full_text = js(session, "document.body.innerText")
    
    return full_text

def extract_posts_from_text(text):
    """Parse raw text into individual posts."""
    posts = []
    # Split by common delimiters
    lines = text.split('\n')
    current_post = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_post and len('\n'.join(current_post)) > 30:
                posts.append('\n'.join(current_post))
                current_post = []
            continue
        current_post.append(line)
    
    if current_post and len('\n'.join(current_post)) > 30:
        posts.append('\n'.join(current_post))
    
    return posts

# Main
SESSION = "boardroom_scrape"

print("=== AI Profit Boardroom Community Scraper ===")
print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Get the feed
print("[1/3] Fetching community feed...")
nav(SESSION, "https://www.skool.com/ai-profit-lab-7462", wait=10)
feed_text = js(SESSION, "document.body.innerText")

# Save raw feed
output_dir = "/home/tom/Desktop/coaching_call/community_scrapes"
os.makedirs(output_dir, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M")

with open(f"{output_dir}/raw_feed_{timestamp}.txt", "w") as f:
    f.write(feed_text)

print(f"Raw feed saved: {len(feed_text)} chars")

# Extract posts
print("[2/3] Extracting posts...")
posts = extract_posts_from_text(feed_text)

# Filter for useful posts (tool mentions, advice, workflows)
keywords = [
    "tool", "agent", "automat", "workflow", "seo", "memory", "blog",
    "scrape", "claude", "codex", "gemini", "chatgpt", "openai",
    "supabase", "lovable", "replit", "bolt", "v0", "cursor",
    "n8n", "zapier", "make", "api", "mcp", "rag", "vector",
    "ranking", "local seo", "google maps", "content", "pipeline",
    "profit", "revenue", "client", "scale", "automation"
]

useful_posts = []
for post in posts:
    post_lower = post.lower()
    score = sum(1 for kw in keywords if kw in post_lower)
    if score >= 2 and len(post) > 80:
        useful_posts.append((score, post))

useful_posts.sort(reverse=True)

# Save filtered posts
with open(f"{output_dir}/useful_posts_{timestamp}.txt", "w") as f:
    f.write(f"AI Profit Boardroom — Useful Posts\n")
    f.write(f"Scraped: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total posts found: {len(posts)}\n")
    f.write(f"Useful posts: {len(useful_posts)}\n")
    f.write("=" * 60 + "\n\n")
    
    for i, (score, post) in enumerate(useful_posts[:50], 1):
        f.write(f"--- Post #{i} (relevance: {score}) ---\n")
        f.write(post[:1000])
        f.write("\n\n")

print(f"Useful posts saved: {len(useful_posts)}")

# Also scroll to get more content
print("[3/3] Scrolling for more content...")
for i in range(5):
    js(SESSION, "window.scrollBy(0, 3000)")
    time.sleep(3)

more_text = js(SESSION, "document.body.innerText")
more_posts = extract_posts_from_text(more_text)

# Add any new useful posts
existing_texts = set(p[1][:100] for p in useful_posts)
new_count = 0
for post in more_posts:
    post_lower = post.lower()
    score = sum(1 for kw in keywords if kw in post_lower)
    if score >= 2 and len(post) > 80 and post[:100] not in existing_texts:
        useful_posts.append((score, post))
        existing_texts.add(post[:100])
        new_count += 1

# Rewrite with all posts
useful_posts.sort(reverse=True)
with open(f"{output_dir}/useful_posts_{timestamp}.txt", "w") as f:
    f.write(f"AI Profit Boardroom — Useful Posts\n")
    f.write(f"Scraped: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Total posts found: {len(posts) + len(more_posts)}\n")
    f.write(f"Useful posts: {len(useful_posts)}\n")
    f.write("=" * 60 + "\n\n")
    
    for i, (score, post) in enumerate(useful_posts[:75], 1):
        f.write(f"--- Post #{i} (relevance: {score}) ---\n")
        f.write(post[:1000])
        f.write("\n\n")

print(f"Added {new_count} more posts from scrolling")
print(f"Total useful posts: {len(useful_posts)}")
print(f"Saved to: {output_dir}/useful_posts_{timestamp}.txt")

# Clean up
wb(SESSION, "close_session")
print("\n=== DONE ===")
