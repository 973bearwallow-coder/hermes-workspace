#!/usr/bin/env python3
"""
Social Media & Web Scraper Wrapper
Uses snscrape (free, no API keys) and Scrapy (powerful crawling)

Usage examples:
  python3 scrape_social.py twitter --query "dog grooming near me" --limit 50
  python3 scrape_social.py reddit --query "pets" --limit 50  
  python3 scrape_social.py tiktok --query "pet care" --limit 30
"""

import sys
import json
import argparse
from datetime import datetime

SCRAPING_VENV = "/home/tom/hermes-workspace/venvs/scraping/bin/python3"

def scrape_twitter(query, limit=50):
    import snscrape.modules.twitter as sntwitter
    results = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "date": str(tweet.date),
            "user": tweet.user.username,
            "content": tweet.content[:500],
            "url": tweet.url,
            "likes": tweet.likeCount,
            "retweets": tweet.retweetCount,
        })
    return results

def scrape_reddit(query, limit=50):
    import snscrape.modules.reddit as snreddit
    results = []
    for i, post in enumerate(snreddit.RedditSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "date": str(post.date),
            "title": post.title,
            "content": (post.selftext or "")[:500],
            "url": post.url,
            "score": post.score,
            "comments": post.numComments,
        })
    return results

def scrape_tiktok(query, limit=30):
    import snscrape.modules.tiktok as sntiktok
    results = []
    for i, post in enumerate(sntiktok.TikTokSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "date": str(post.date),
            "user": post.user.username,
            "content": (post.title or "")[:500],
            "url": post.url,
        })
    return results

def main():
    parser = argparse.ArgumentParser(description="Social media scraper")
    parser.add_argument("platform", choices=["twitter", "reddit", "tiktok"], help="Platform to scrape")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Max results (default: 50)")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    parser.add_argument("--pet-keywords", action="store_true", help="Use pet industry keywords for content research")
    
    args = parser.parse_args()
    
    if args.pet_keywords:
        # Pet industry content research mode
        queries = [
            f"{args.query} pet",
            f"{args.query} dog",
            f"{args.query} cat",
            f"{args.query} pet care",
        ]
    else:
        queries = [args.query]
    
    all_results = []
    for q in queries:
        print(f"Scraping {args.platform}: {q}...", file=sys.stderr)
        if args.platform == "twitter":
            results = scrape_twitter(q, args.limit // len(queries))
        elif args.platform == "reddit":
            results = scrape_reddit(q, args.limit // len(queries))
        elif args.platform == "tiktok":
            results = scrape_tiktok(q, args.limit // len(queries))
        all_results.extend(results)
        print(f"  Got {len(results)} results", file=sys.stderr)
    
    output = {
        "platform": args.platform,
        "query": args.query,
        "scraped_at": str(datetime.now()),
        "count": len(all_results),
        "results": all_results,
    }
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved {len(all_results)} results to {args.output}")
    else:
        print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
