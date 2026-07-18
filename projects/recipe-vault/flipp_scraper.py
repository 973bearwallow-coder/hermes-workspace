#!/usr/bin/env python3
"""
Flipp grocery flyer scraper for Atlas / recipe-vault.

Pulls weekly sale prices for Harris Teeter, Giant Food, and Safeway in
Falls Church, VA (ZIP 22046) from Flipp's public aggregator API. One
source covers all three stores.

API (reverse-engineered from github.com/dohougroup/flyer-scraper):
    Base:   https://backflipp.wishabi.com/flipp
    Flyers: GET /flyers?postal_code=<ZIP>          -> list of flyers by merchant
    Items:  GET /items/search?flyer_ids=<ID>&postal_code=<ZIP> -> flyer items w/ prices

The Canadian repo used postal codes; Flipp's API works fine with US ZIP
codes too (verified: 22046 returns real US merchants).

Usage:
    python3 flipp_scraper.py            # full scrape -> flipp_prices.json
    python3 flipp_scraper.py --test     # print first 5 items, no file write
"""

import sys
import json
import time
import argparse
from datetime import datetime, timezone

import requests

BASE_URL = "https://backflipp.wishabi.com/flipp"
ZIP_CODE = "22046"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
OUT_PATH = "/home/tom/hermes-workspace/projects/recipe-vault/flipp_prices.json"

# Flipp merchant_name -> our normalized store key.
# Matched case-insensitively via substring on the flyer merchant name.
TARGET_STORES = {
    "harris teeter": "harris_teeter",
    "giant food": "giant",
    "safeway": "safeway",
}

REQUEST_DELAY = 0.6   # polite delay between item requests (seconds)
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0   # seconds, multiplied by attempt number


def _get(url, params=None):
    """HTTP GET with retries on 429 / timeout / 5xx."""
    headers = {"User-Agent": UA, "Accept": "application/json"}
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=25)
            if r.status_code == 429:
                wait = RETRY_BACKOFF * attempt
                print(f"    [429] rate limited, waiting {wait:.1f}s "
                      f"(attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            if r.status_code >= 500:
                wait = RETRY_BACKOFF * attempt
                print(f"    [{r.status_code}] server error, retry in {wait:.1f}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except (requests.Timeout, requests.ConnectionError) as e:
            last_err = e
            wait = RETRY_BACKOFF * attempt
            print(f"    [timeout/conn] {e}; retry in {wait:.1f}s "
                  f"(attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)
        except Exception as e:
            last_err = e
            break
    print(f"    request failed after {MAX_RETRIES} attempts: {last_err}")
    return None


def fetch_flyers(zip_code):
    """Return list of flyer dicts for the ZIP."""
    data = _get(f"{BASE_URL}/flyers", params={"postal_code": zip_code})
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("flyers", [])


def match_store(merchant_name):
    """Return normalized store key if merchant is a target, else None."""
    if not merchant_name:
        return None
    low = merchant_name.lower()
    for needle, key in TARGET_STORES.items():
        if needle in low:
            return key
    return None


def _to_float(v):
    if v is None:
        return None
    try:
        f = float(v)
        return f
    except (TypeError, ValueError):
        return None


def fetch_items(flyer_id, zip_code):
    """Return raw item list for a flyer (handles dict/list responses)."""
    data = _get(f"{BASE_URL}/items/search",
                params={"flyer_ids": flyer_id, "postal_code": zip_code})
    if not data:
        return []
    if isinstance(data, list):
        return data
    return data.get("items") or data.get("ecom_items") or []


def normalize_item(item, store_key, flyer):
    """Map a raw Flipp item to our schema."""
    # Prices: current_price may be a bare number; pre_price_text like '2/'
    # signals a multi-buy (e.g. "2/$3"). We keep current_price as-is and
    # preserve pre_price_text in the price note.
    cur = _to_float(item.get("current_price") or item.get("sale_price")
                    or item.get("price"))
    orig = _to_float(item.get("original_price") or item.get("regular_price"))

    pre = item.get("pre_price_text")
    post = item.get("post_price_text")
    price_note_parts = [p for p in (pre, post) if p]
    price_note = " ".join(price_note_parts) if price_note_parts else None

    valid_from = item.get("valid_from") or flyer.get("valid_from") or ""
    valid_to = item.get("valid_to") or flyer.get("valid_to") or ""
    flyer_valid_dates = None
    if valid_from or valid_to:
        flyer_valid_dates = f"{valid_from} -> {valid_to}".strip()

    return {
        "store": store_key,
        "product_name": item.get("name") or item.get("title") or "Unknown Product",
        "current_price": cur,
        "original_price": orig,
        "price_note": price_note,          # e.g. "2/" for 2/$3 deals
        "sale_story": item.get("sale_story") or None,
        "category": item.get("category") or item.get("category_name") or None,
        "flyer_valid_dates": flyer_valid_dates,
        "flyer_id": flyer.get("id"),
        "merchant_name": item.get("merchant_name") or flyer.get("merchant"),
    }


def scrape(zip_code):
    """Main scrape. Returns dict keyed by normalized store -> [items]."""
    print(f"Fetching flyers for ZIP {zip_code} ...")
    flyers = fetch_flyers(zip_code)
    print(f"Found {len(flyers)} total flyers for {zip_code}.")

    # Collect target flyers grouped by store.
    target_flyers = []
    for f in flyers:
        merchant = f.get("merchant") or f.get("name")
        key = match_store(merchant)
        if key:
            target_flyers.append((key, merchant, f))

    print(f"Matched {len(target_flyers)} target flyers "
          f"(harris_teeter / giant / safeway):")
    for key, merchant, f in target_flyers:
        print(f"  - {merchant} (id={f.get('id')}) -> {key}")

    stores = {"harris_teeter": [], "giant": [], "safeway": []}

    for key, merchant, flyer in target_flyers:
        fid = flyer.get("id")
        print(f"\nFetching items: {merchant} (flyer {fid}) ...")
        items = fetch_items(fid, zip_code)
        print(f"  {len(items)} raw items")
        for it in items:
            stores[key].append(normalize_item(it, key, flyer))
        time.sleep(REQUEST_DELAY)

    return stores


def print_summary(stores):
    print("\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)
    total = 0
    for key in ("harris_teeter", "giant", "safeway"):
        items = stores.get(key, [])
        total += len(items)
        print(f"\n{key}: {len(items)} items")
        for it in items[:2]:
            price = it["current_price"]
            note = f" [{it['price_note']}]" if it.get("price_note") else ""
            print(f"    - {it['product_name']}"
                  f" | ${price}{note}"
                  f" | {it.get('sale_story') or ''}")
    print(f"\nTOTAL items across 3 stores: {total}")


def run_test(zip_code):
    """--test: print first 5 items across all stores, no file write."""
    stores = scrape(zip_code)
    flat = []
    for key in ("harris_teeter", "giant", "safeway"):
        flat.extend(stores[key])
    print("\n" + "=" * 55)
    print("TEST MODE - first 5 items across all stores")
    print("=" * 55)
    for it in flat[:5]:
        print(json.dumps(it, indent=2))
    print(f"\n(total collected: {len(flat)} items; no file written)")
    return stores


def main():
    ap = argparse.ArgumentParser(description="Flipp flyer scraper (22046)")
    ap.add_argument("--test", action="store_true",
                    help="print first 5 items, do not write JSON file")
    ap.add_argument("--zip", default=ZIP_CODE, help="ZIP code (default 22046)")
    args = ap.parse_args()

    if args.test:
        run_test(args.zip)
        return

    stores = scrape(args.zip)
    print_summary(stores)

    payload = {
        "zip": args.zip,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "source": "flipp (backflipp.wishabi.com)",
        "stores": stores,
    }
    with open(OUT_PATH, "w") as fh:
        json.dump(payload, fh, indent=2)
    print(f"\nWrote {OUT_PATH}")

    # Optional shared memory bridge (best-effort, non-fatal).
    try:
        sys.path.insert(0, "/home/tom/hermes-workspace/memory")
        from memory_bridge import log_subbot  # type: ignore
        total = sum(len(v) for v in stores.values())
        log_subbot("flipp_scraper",
                   f"Scraped {total} items from Flipp for ZIP {args.zip}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
