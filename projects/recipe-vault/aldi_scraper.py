#!/usr/bin/env python3
"""
Aldi Weekly Specials price scraper (Falls Church, VA — store FRE 69, ZIP 22042).

Uses Playwright headless Chromium to render the Aldi weekly-specials page,
dismisses the "How would you like to shop?" dialog (click In-Store + Confirm),
then extracts Price Drops / Weekly Ad product cards into a structured JSON file.

Product cards are reliably identified by:
    div[role="group"][aria-label="Product"]
within which:
    - product name  -> div[role="heading"]
    - "Current price: $X.XX" / "Original Price: $Y.YY" / "N% off"
                        -> .screen-reader-only spans (full text in DOM)

Usage:
    python3 aldi_scraper.py            # full run, writes aldi_prices.json
    python3 aldi_scraper.py --test     # print first 5 items, no file write
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

STORE = "ALDI - FRE 69 - Falls Church"
ZIP_CODE = "22042"
URL = "https://www.aldi.us/weekly-specials/"
OUT_PATH = "/home/tom/hermes-workspace/projects/recipe-vault/aldi_prices.json"
# Discovered from the live ALDI store session for FRE 69 / Falls Church.
SHOP_ID = "23754"
ZONE_ID = "975"

PRICE_RE = re.compile(r"\$[\s]*([\d,]+\.\d{2})")
PCT_RE = re.compile(r"(\d+)\s*%\s*off")


def click_by_text(page, text, timeout=8000):
    """Click an element whose visible text contains `text`. Tries get_by_text
    first, then falls back to a button/link/role=button ancestor."""
    try:
        page.get_by_text(text, exact=False).first.click(timeout=timeout)
        return True
    except Exception:
        try:
            loc = page.locator("button, a, [role='button']", has_text=text).first
            loc.click(timeout=timeout)
            return True
        except Exception:
            # last resort: click nearest clickable ancestor of a text span
            try:
                span = page.locator(f"*:has-text('{text}')").first
                span.locator(
                    "xpath=ancestor::*[self::button or self::a or @role='button'][1]"
                ).click(timeout=timeout)
                return True
            except Exception:
                return False


def parse_card(card):
    """Parse a product card element into a structured dict."""
    item: dict[str, object] = {
        "name": None,
        "current_price": None,
        "original_price": None,
        "discount_pct": None,
        "category": None,
    }
    try:
        full = card.inner_text(timeout=4000)
    except Exception:
        return item
    full = " ".join(full.split())

    # Product name: ALDI currently renders an h3 and an image alt; older
    # versions exposed role=heading. Try all three in stable order.
    for selector, attribute in (
        ("[role='heading']", None),
        ("h3", None),
        ("img[data-testid='item-card-image']", "alt"),
    ):
        try:
            loc = card.locator(selector).first
            name = loc.get_attribute(attribute) if attribute else loc.inner_text(timeout=2000)
            name = " ".join((name or "").split())
            if name:
                item["name"] = name
                break
        except Exception:
            continue

    # prices + discount from screen-reader text
    prices = PRICE_RE.findall(full)
    if len(prices) >= 1:
        item["current_price"] = float(prices[0].replace(",", ""))
    if len(prices) >= 2:
        item["original_price"] = float(prices[1].replace(",", ""))

    m = PCT_RE.search(full)
    if m:
        item["discount_pct"] = int(m.group(1))

    # category: try a label containing 'in stock' suffix or breadcrumb; best-effort
    cat = None
    # some cards expose category via aria or nearby text like "Many in stock"
    # leave None if not determinable (kept explicit/null per spec)
    item["category"] = cat
    return item


def extract_items(page):
    """Extract all product cards currently in the DOM."""
    items = []
    seen = set()
    try:
        cards = page.locator("div[role='group'][aria-label='Product']").all()
    except Exception:
        cards = []
    for c in cards:
        parsed = parse_card(c)
        if parsed["current_price"] is None:
            continue
        key = parsed["name"] or parsed["current_price"]
        if key in seen:
            continue
        seen.add(key)
        items.append(parsed)
    return items


def extract_item_ids(page):
    """Collect all ALDI item IDs embedded in the rendered page source."""
    try:
        html = page.content()
    except Exception:
        return []
    return sorted(set(re.findall(r"items_\d+-\d+", html)))


def _parse_money(text):
    if not text:
        return None
    m = re.search(r"\$\s*([\d,]+(?:\.\d{2})?)", str(text))
    if not m:
        return None
    try:
        return float(m.group(1).replace(",", ""))
    except Exception:
        return None


def normalize_api_item(item):
    """Map an ALDI GraphQL item object into the JSON schema we store."""
    price = item.get("price") or {}
    view = price.get("viewSection") or {}
    card = view.get("itemCard") or {}
    details = view.get("itemDetails") or {}

    current_text = (
        card.get("priceString")
        or details.get("priceString")
        or price.get("priceString")
        or card.get("priceAriaLabelString")
    )
    original_text = (
        card.get("fullPriceString")
        or card.get("plainFullPriceString")
        or details.get("fullPriceString")
        or details.get("fullPriceScreenReaderString")
    )

    current_price = _parse_money(current_text)
    original_price = _parse_money(original_text)
    discount_pct = None
    if current_price is not None and original_price is not None and original_price > 0:
        try:
            discount_pct = round((original_price - current_price) / original_price * 100)
        except Exception:
            discount_pct = None

    category = None
    view_section = item.get("viewSection") or {}
    for key in ("categoryString", "category", "sectionName", "nameString"):
        if view_section.get(key):
            category = view_section.get(key)
            break

    return {
        "name": item.get("name") or None,
        "current_price": current_price,
        "original_price": original_price,
        "discount_pct": discount_pct,
        "category": category,
    }


def fetch_items_api(page, ids, shop_id=SHOP_ID, zone_id=ZONE_ID, postal_code=ZIP_CODE):
    """Fetch ALDI item details from GraphQL in manageable batches."""
    items = []
    batch_size = 30
    total = len(ids)
    for i in range(0, total, batch_size):
        batch = ids[i:i + batch_size]
        resp = page.evaluate(
            """async ({ids, shopId, zoneId, postalCode}) => {
              const vars = {ids, shopId, zoneId, postalCode};
              const url = 'https://www.aldi.us/graphql?operationName=Items&variables=' +
                encodeURIComponent(JSON.stringify(vars)) + '&extensions=' +
                encodeURIComponent(JSON.stringify({persistedQuery:{version:1, sha256Hash:'388f200246a7fcc0f10ed9c1bb97952f9046e69c1be3b14ebae5855822cec831'}}));
              const r = await fetch(url, {headers: {'accept': 'application/json'}});
              if (!r.ok) throw new Error(`HTTP ${r.status} for Items batch`);
              return await r.json();
            }""",
            {"ids": batch, "shopId": shop_id, "zoneId": zone_id, "postalCode": postal_code},
        )
        batch_items = (resp or {}).get("data", {}).get("items") or []
        print(f"[api] batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size}: {len(batch_items)} items", file=sys.stderr)
        items.extend(batch_items)
    return items


def try_weekly_ad(page, items):
    """Attempt to expand the full Weekly Ad via a 'View all' style button."""
    for label in ["View all", "View Weekly Ad", "See all", "View all (200+)"]:
        if click_by_text(page, label, timeout=4000):
            page.wait_for_timeout(2500)
            for _ in range(4):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1000)
            extra = extract_items(page)
            existing = {it.get("name") for it in items}
            added = 0
            for it in extra:
                if it.get("name") and it["name"] not in existing:
                    items.append(it)
                    existing.add(it["name"])
                    added += 1
            print(f"[weekly-ad] clicked '{label}': +{added} items", file=sys.stderr)
            return items
    return items


def run(test_mode=False):
    items = []
    error = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        page.set_default_timeout(20000)

        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(2500)

            # Cookie dialog
            click_by_text(page, "Accept All", timeout=4000)
            page.wait_for_timeout(600)

            # "How would you like to shop?" -> In-Store -> Confirm
            click_by_text(page, "In-Store", timeout=7000)
            page.wait_for_timeout(1000)
            click_by_text(page, "Confirm", timeout=7000)
            page.wait_for_timeout(3000)

            # Wait for Price Drops section to populate
            try:
                page.get_by_text("Price Drops").first.wait_for(timeout=15000)
            except PWTimeout:
                pass

            # Scroll to trigger lazy-loading of carousel items
            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1200)

            ids = extract_item_ids(page)
            if ids:
                print(f"[api] found {len(ids)} embedded item ids", file=sys.stderr)
                raw_items = fetch_items_api(page, ids)
                items = [normalize_api_item(it) for it in raw_items if it]
                deduped = []
                seen = set()
                for it in items:
                    key = (it.get("name"), it.get("current_price"), it.get("original_price"))
                    if key in seen:
                        continue
                    seen.add(key)
                    deduped.append(it)
                items = deduped
                # The ALDI Items API sometimes returns upcoming/unavailable
                # products with names but no prices. Treat that as unusable and
                # fall back to the rendered, store-selected product cards.
                if not any(it.get("current_price") is not None for it in items):
                    print("[api] returned no priced items; falling back to rendered cards", file=sys.stderr)
                    items = extract_items(page)
                    items = try_weekly_ad(page, items)
            else:
                items = extract_items(page)

            if not items and not test_mode:
                items = extract_items(page)

        except Exception as e:
            error = f"{type(e).__name__}: {e}"
        finally:
            try:
                browser.close()
            except Exception:
                pass  # never hang on close

    if test_mode:
        print(f"TEST MODE — extracted {len(items)} items (showing first 5):")
        for it in items[:5]:
            print(json.dumps(it, ensure_ascii=False))
        return {"ran": True, "count": len(items), "path": None, "error": error}

    payload = {
        "store": STORE,
        "zip": ZIP_CODE,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(items)} items -> {OUT_PATH}")
    for it in items[:3]:
        print("  " + json.dumps(it, ensure_ascii=False))
    return {"ran": True, "count": len(items), "path": OUT_PATH, "error": error}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="print first 5 items only")
    args = ap.parse_args()
    result = run(test_mode=args.test)
    if result["error"]:
        print(f"ERROR: {result['error']}", file=sys.stderr)


if __name__ == "__main__":
    main()
