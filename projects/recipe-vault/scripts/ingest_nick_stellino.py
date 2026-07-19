#!/usr/bin/env python3
"""
ingest_nick_stellino.py — Scrape Nick Stellino's recipe site and add pasta
recipes to the vault. Clean HTML (no OCR). Tagged "Nick Stellino".

USAGE:
  python3 ingest_nick_stellino.py --category pasta
  python3 ingest_nick_stellino.py --url https://nickstellino.com/recipe/pasta-e-fagioli/
  python3 ingest_nick_stellino.py --category pasta --dry-run

HEADERS: site blocks plain curl; send a browser UA.
"""
import sys, os, re, html, json, argparse
import urllib.request

VAULT = "/home/tom/hermes-workspace/projects/recipe-vault"
RECIPES = os.path.join(VAULT, "recipes")
CAT_BASE = "https://nickstellino.com/recipe_category/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

def get_recipe_links(category):
    url = CAT_BASE + category + "/"
    html_text = fetch(url)
    links = set(re.findall(r'href="(https://nickstellino\.com/recipe/[^"#]+)"', html_text))
    return sorted(links)

def parse_recipe(url):
    t = fetch(url)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", t)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)

    # Title = from URL slug
    slug = url.rstrip("/").split("/")[-1]
    title = slug.replace("-", " ").title().replace(" E ", " e ").replace(" Al ", " al ")

    # Ingredients block
    idx = text.lower().find("ingredients:")
    if idx < 0:
        idx = text.lower().find("ingredient")
    ing_text = ""
    if idx >= 0:
        # cut at next major section keyword or "Type of Products" footer
        cut = len(text)
        for kw in ["type of products", "instructions:", "directions:", "method:"]:
            j = text.lower().find(kw, idx+10)
            if j > idx and j < cut:
                cut = j
        ing_text = text[idx:cut]

    return {"title": title, "url": url, "ingredients": ing_text.strip(), "raw": text[:200]}

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

def bullet_ingredients(flat):
    """Convert a flat 'Ingredients: ...' paragraph into bulleted markdown lines.
    Splits on common boundaries: leading quantity+unit, or ' Ingredients: ' seg."""
    flat = re.sub(r"^ingredients:\s*", "", flat, flags=re.I)
    # split on digit-led quantity starts (e.g. '3 tbsp oil 1 cup flour')
    parts = re.split(r"(?=(?:\d|\d\s*\d*/\d|½|¼|¾|⅓|⅔|⅛|\ba\b|\ban\b|\bsome\b|\ba pinch\b)\s)", flat)
    bullets = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # skip nav/footer debris
        if re.search(r"type of products|advertisement|nutrition|serves:", p, re.I):
            continue
        if len(p) < 2:
            continue
        bullets.append(f"- {p}")
    return "\n".join(bullets) if bullets else flat

def write_recipe(rec, dry_run):
    slug = slugify(rec["title"])
    bullets = bullet_ingredients(rec["ingredients"])
    fm = f"# {rec['title']}\n\n**Source:** Nick Stellino\n**URL:** {rec['url']}\n\n## Ingredients\n\n{bullets}\n\n## Instructions\n\n(See source URL — full steps on nickstellino.com)\n"
    if dry_run:
        return f"[DRY] {rec['title']} ({len(rec['ingredients'])} chars ingredients)"
    path = os.path.join(RECIPES, f"{slug}-nickstellino.md")
    with open(path, "w") as f:
        f.write(fm)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default="pasta")
    ap.add_argument("--url")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.url:
        links = [a.url]
    else:
        links = get_recipe_links(a.category)
        print(f"Found {len(links)} recipes in category '{a.category}'")

    os.makedirs(RECIPES, exist_ok=True)
    written = 0
    for link in links:
        try:
            rec = parse_recipe(link)
            res = write_recipe(rec, a.dry_run)
            print(res)
            written += 1
        except Exception as e:
            print(f"FAIL {link}: {e}")
    print(f"\nDone. {written} recipes processed.")
    if not a.dry_run and written:
        print("Run: cd", VAULT, "&& /home/tom/.hermes/hermes-agent/venv/bin/python3 rebuild_ingredient_index.py")

if __name__ == "__main__":
    main()
