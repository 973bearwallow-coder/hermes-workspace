#!/usr/bin/env python3
"""Lidl flyer OCR scraper — screenshot each page, OCR with tesseract, extract prices."""
import json, re, sys, time
from datetime import datetime, timezone
from PIL import Image
import pytesseract
from playwright.sync_api import sync_playwright

URL = "https://www.lidl.com/flyer/esi-flyer/weekly-ad-7-22-2026-7-28-2026-ac70cb/view/flyer/page/1"
OUT = "/home/tom/hermes-workspace/projects/recipe-vault/lidl_prices.json"
TMP = "/tmp/lidl_pages"
import os
os.makedirs(TMP, exist_ok=True)

PRICE_RE = re.compile(r"\$\s*([\d,]+\.\d{2})")
URL_RE = re.compile(r"https?://\S+")

def ocr_page(img_path):
    img = Image.open(img_path)
    w, h = img.size
    # OCR full image at higher resolution (upscale 2x for tesseract accuracy)
    img = img.resize((w * 2, h * 2))
    text = pytesseract.image_to_string(img, config="--psm 11")
    items = []
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for i, line in enumerate(lines):
        line = URL_RE.sub("", line).strip()
        m = PRICE_RE.search(line)
        if not m:
            continue
        price = float(m.group(1).replace(",", ""))
        # product name = nearest non-price line above
        name = ""
        for j in range(i - 1, max(-1, i - 5), -1):
            if not PRICE_RE.search(lines[j]) and len(lines[j]) > 2:
                name = lines[j]
                break
        if name:
            items.append({"product_name": name[:80], "price": price, "raw": line[:120]})
    return items

def main():
    items = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        pg = b.new_page(viewport={"width": 1400, "height": 1000})
        pg.goto(URL, wait_until="domcontentloaded", timeout=30000)
        pg.wait_for_timeout(2000)
        # consent
        try:
            pg.get_by_text("Agree All").first.click(timeout=5000)
            pg.wait_for_timeout(1500)
        except Exception:
            pass
        for page_num in range(1, 49):
            try:
                pg.wait_for_timeout(1200)
                path = f"{TMP}/page_{page_num:02d}.png"
                pg.screenshot(path=path)
                found = ocr_page(path)
                for it in found:
                    it["page"] = page_num
                    items.append(it)
                print(f"[page {page_num}] +{len(found)} items (total {len(items)})", file=sys.stderr)
            except Exception as e:
                print(f"[page {page_num}] err: {e}", file=sys.stderr)
                break
        try:
            b.close()
        except Exception:
            pass

    payload = {
        "store": "lidl",
        "zip": None,
        "flyer_dates": "2026-07-22..2026-07-28",
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"DONE: {len(items)} items -> {OUT}")

if __name__ == "__main__":
    main()
