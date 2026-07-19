#!/usr/bin/env python3
"""ingest_atk_2008.py — Add recipes from America's Test Kitchen 2008 Best of the Year
book that are freely available online (the book itself is Archive.org borrow-only).
Currently: Vietnamese Caramel Catfish (Ca Kho To) — ATK's 2008 adaptation.
"""
import os, re, html
import urllib.request

VAULT = "/home/tom/hermes-workspace/projects/recipe-vault"
RECIPES = os.path.join(VAULT, "recipes")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30).read().decode("utf-8", "ignore")

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

def bullet_ingredients(flat):
    flat = re.sub(r"^ingredients:\s*", "", flat, flags=re.I)
    parts = re.split(r"(?=(?:\d|\d\s*\d*/\d|½|¼|¾|⅓|⅔|⅛|\ba\b|\ban\b|\bsome\b|\ba pinch\b)\s)", flat)
    bullets = []
    for p in parts:
        p = p.strip()
        if not p or len(p) < 2:
            continue
        if re.search(r"type of products|advertisement|nutrition|serves:|recipe from|provided by|buy all ingredients", p, re.I):
            continue
        bullets.append(f"- {p}")
    return "\n".join(bullets) if bullets else flat

def extract(url, title, source_tag):
    t = fetch(url)
    t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", "", t, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", t)
    txt = html.unescape(txt); txt = re.sub(r"\s+", " ", txt)
    i = txt.lower().find("ingredient")
    ing = txt[i:i+900] if i > 0 else "(ingredients not parsed — see source URL)"
    bullets = bullet_ingredients(ing)
    fm = f"# {title}\n\n**Source:** America's Test Kitchen 2008 Best of the Year (via {source_tag})\n**URL:** {url}\n\n## Ingredients\n\n{bullets}\n\n## Instructions\n\n(Full steps at source URL)\n"
    return fm

def main():
    recipes = [
        ("ATK 2008 Vietnamese Caramel Catfish (Ca Kho To)",
         "https://www.tfrecipes.com/ca-kho-to-vietnamese-caramelized-fish/", "tfrecipes"),
    ]
    os.makedirs(RECIPES, exist_ok=True)
    for title, url, tag in recipes:
        fm = extract(url, title, tag)
        path = os.path.join(RECIPES, f"{slugify(title)}-atk2008.md")
        with open(path, "w") as f:
            f.write(fm)
        print(f"wrote {path}")

if __name__ == "__main__":
    main()
