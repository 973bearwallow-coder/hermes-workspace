#!/usr/bin/env python3
"""
Reddit Pet Industry Scraper v2
Scrapes pet-related subreddits for content research.
Uses old.reddit.com HTML scraping — no API key needed.

Usage:
  python3 reddit_pet_scraper.py --subreddits dogs,cats --limit 50
  python3 reddit_pet_scraper.py --trending --limit 100
  python3 reddit_pet_scraper.py --category dogs --limit 50
  python3 reddit_pet_scraper.py --all-pets --limit 200
"""

import requests
from bs4 import BeautifulSoup
import json
import argparse
import time
import re
from datetime import datetime

# Pet industry subreddits organized by category
PET_SUBREDDITS = {
    "general": ["petcare", "pets", "animals"],
    "dogs": ["dogs", "dogtraining", "puppy101", "reactivedogs", "DogAdvice", "dogfree"],
    "cats": ["cats", "catadvice", "kittens", "CatTraining"],
    "grooming": ["doggrooming", "PetGrooming"],
    "health": ["vet", "AskVet", "pethealth", "doghealth"],
    "business": ["smallbusiness", "Entrepreneur", "sidehustle"],
    "services": ["dogwalking", "petsitting"],
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()[:2000]

def parse_post(post_soup):
    try:
        title_elem = post_soup.find("a", {"data-event-action": "title"})
        if not title_elem:
            title_elem = post_soup.find("a", class_="title")
        if not title_elem:
            return None

        title = clean_text(title_elem.get_text())
        if not title or len(title) < 5:
            return None

        url = title_elem.get("href", "")
        if url and not url.startswith("http"):
            url = f"https://old.reddit.com{url}"

        score_elem = post_soup.find("div", class_="score")
        score = 0
        if score_elem:
            score_text = score_elem.get("title", score_elem.get_text())
            score = int(re.sub(r'[^\d]', '', str(score_text)) or 0)

        comments_elem = post_soup.find("a", class_="comments")
        comments = 0
        if comments_elem:
            match = re.search(r'(\d+)', comments_elem.get_text())
            if match:
                comments = int(match.group(1))

        subreddit_elem = post_soup.find("a", class_="subreddit")
        subreddit = subreddit_elem.get_text().replace("r/", "") if subreddit_elem else ""

        time_elem = post_soup.find("time")
        post_time = time_elem.get("datetime", time_elem.get_text()) if time_elem else ""

        body_elem = post_soup.find("div", class_="md")
        body = clean_text(body_elem.get_text()) if body_elem else ""

        return {
            "title": title, "url": url, "score": score,
            "comments": comments, "subreddit": subreddit,
            "time": post_time, "body": body,
        }
    except:
        return None

def scrape_subreddit(subreddit, sort="hot", limit=50):
    posts = []
    url = f"https://old.reddit.com/r/{subreddit}/{sort}/"
    pages = max(1, limit // 25)

    for page in range(pages):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                break

            soup = BeautifulSoup(r.text, "html.parser")
            post_elements = soup.find_all("div", {"data-context": "listing"})
            if not post_elements:
                post_elements = soup.find_all("div", class_="thing")

            if not post_elements:
                break

            for post_el in post_elements:
                post = parse_post(post_el)
                if post:
                    posts.append(post)

            next_btn = soup.find("span", class_="next-button")
            if next_btn and next_btn.find("a"):
                href = next_btn.find("a").get("href", "")
                url = href if href.startswith("http") else f"https://old.reddit.com{href}"
            else:
                break

            if len(posts) >= limit:
                break

            time.sleep(2)
        except:
            break

    return posts[:limit]

def analyze_trends(posts):
    from collections import Counter
    questions = []
    topics = []

    pet_keywords = [
        "best", "recommend", "review", "vs", "how to", "what is", "why",
        "tips", "guide", "cheap", "affordable", "durable", "waterproof",
        "safe", "organic", "natural", "grooming", "training", "health",
        "food", "treats", "toys", "harness", "leash", "collar", "bed",
        "crate", "puppy", "kitten", "senior", "anxiety", "allergies",
    ]

    for post in posts:
        title = post.get("title", "")
        body = post.get("body", "")

        if "?" in title:
            questions.append(title)

        text = f"{title} {body}".lower()
        for kw in pet_keywords:
            if kw in text:
                topics.append(kw)

    topic_counts = Counter(topics).most_common(20)

    return {
        "top_topics": [{"topic": t, "count": c} for t, c in topic_counts],
        "questions": questions[:30],
        "total_posts_analyzed": len(posts),
    }

def main():
    parser = argparse.ArgumentParser(description="Reddit Pet Industry Scraper")
    parser.add_argument("--subreddits", "-s", help="Comma-separated subreddit names")
    parser.add_argument("--category", "-c", choices=list(PET_SUBREDDITS.keys()), help="Predefined category")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Max posts per subreddit")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--trending", "-t", action="store_true", help="Scrape trending pet subreddits")
    parser.add_argument("--all-pets", action="store_true", help="Scrape all pet subreddits")
    parser.add_argument("--analyze", "-a", action="store_true", help="Analyze trends")

    args = parser.parse_args()

    print(f"🐾 Reddit Pet Industry Scraper — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    all_posts = []

    if args.all_pets:
        all_subs = []
        for subs in PET_SUBREDDITS.values():
            all_subs.extend(subs)
        print(f"📋 Scraping {len(all_subs)} pet subreddits...")
        for sub in all_subs:
            print(f"  r/{sub}...", end=" ", flush=True)
            posts = scrape_subreddit(sub, limit=max(5, args.limit // len(all_subs)))
            all_posts.extend(posts)
            print(f"{len(posts)} posts")
            time.sleep(1)

    elif args.trending:
        subs = ["dogs", "cats", "petcare", "puppy101", "AskVet", "doggrooming"]
        print(f"📈 Scraping {len(subs)} trending pet subreddits...")
        for sub in subs:
            print(f"  r/{sub}...", end=" ", flush=True)
            posts = scrape_subreddit(sub, limit=args.limit // len(subs))
            all_posts.extend(posts)
            print(f"{len(posts)} posts")
            time.sleep(1)

    elif args.category:
        subs = PET_SUBREDDITS[args.category]
        print(f"📂 Category: {args.category} ({', '.join(subs)})")
        for sub in subs:
            print(f"  r/{sub}...", end=" ", flush=True)
            posts = scrape_subreddit(sub, limit=args.limit // len(subs))
            all_posts.extend(posts)
            print(f"{len(posts)} posts")
            time.sleep(1)

    elif args.subreddits:
        subs = [s.strip() for s in args.subreddits.split(",")]
        for sub in subs:
            print(f"  r/{sub}...", end=" ", flush=True)
            posts = scrape_subreddit(sub, limit=args.limit)
            all_posts.extend(posts)
            print(f"{len(posts)} posts")
            time.sleep(1)

    else:
        # Default: key pet subreddits
        subs = ["dogs", "cats", "petcare", "puppy101", "AskVet"]
        print(f"🐕 Default: {', '.join(f'r/{s}' for s in subs)}")
        for sub in subs:
            print(f"  r/{sub}...", end=" ", flush=True)
            posts = scrape_subreddit(sub, limit=args.limit // len(subs))
            all_posts.extend(posts)
            print(f"{len(posts)} posts")
            time.sleep(1)

    # Deduplicate
    seen = set()
    unique = [p for p in all_posts if p["url"] not in seen and not seen.add(p["url"])]

    print(f"\n📊 Total unique posts: {len(unique)}")

    analysis = None
    if args.analyze or len(unique) > 0:
        analysis = analyze_trends(unique)
        print(f"🔬 Top topics: {', '.join(t['topic'] for t in analysis['top_topics'][:10])}")
        print(f"❓ Questions found: {len(analysis['questions'])}")

    output = {
        "scraped_at": str(datetime.now()),
        "total_posts": len(unique),
        "posts": unique,
    }
    if analysis:
        output["trend_analysis"] = analysis

    # Save
    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 Saved: {args.output}")
    else:
        path = f"/home/tom/hermes-workspace/results/pet_trends_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        import os; os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n💾 Saved: {path}")

    # Top posts
    print(f"\n🏆 Top Posts:")
    for i, p in enumerate(sorted(unique, key=lambda x: x.get("score", 0), reverse=True)[:10], 1):
        print(f"  {i}. [{p['score']}] {p['title'][:75]}")
        print(f"     r/{p.get('subreddit', '?')} | {p.get('comments', 0)} comments")

    # Content ideas from questions
    if analysis and analysis["questions"]:
        print(f"\n💡 Content Ideas (from questions):")
        for i, q in enumerate(analysis["questions"][:10], 1):
            print(f"  {i}. {q[:90]}")

    print(f"\n✅ Done!")

if __name__ == "__main__":
    main()
