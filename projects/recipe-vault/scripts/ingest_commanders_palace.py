#!/usr/bin/env python3
"""ingest_commanders_palace.py — add Commander's Palace recipes to vault.
Two known-good sources:
  - Bread Pudding Souffle w/ Whiskey Sauce: Food.com (Commander's Palace)
  - Potato-Crusted Fish: tfrecipes (Commander's-style technique)
"""
import os, re, html, json, argparse
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
        if re.search(r"type of products|advertisement|nutrition|serves:", p, re.I):
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
    fm = f"# {title}\n\n**Source:** Commander's Palace (via {source_tag})\n**URL:** {url}\n\n## Ingredients\n\n{bullets}\n\n## Instructions\n\n(Full steps at source URL)\n"
    return fm

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

def main():
    recipes = [
        ("Commanders Palace Bread Pudding Souffle with Whiskey Sauce",
         "https://www.food.com/recipe/bread-pudding-souffle-with-whiskey-sauce-23774", "Food.com"),
        ("Potato Crusted Fish (Commanders Palace Style)",
         "https://www.tfrecipes.com/potato-crusted-baked-cod/", "tfrecipes"),
        ("Commanders Palace Catfish Pecan with Lemon Thyme Pecan Butter",
         "https://www.tfrecipes.com/catfish-pecan-with-lemon-thyme-pecan-butter/", "tfrecipes"),
    ]
    os.makedirs(RECIPES, exist_ok=True)
    for title, url, tag in recipes:
        fm = extract(url, title, tag)
        path = os.path.join(RECIPES, f"{slugify(title)}-commanders.md")
        with open(path, "w") as f:
            f.write(fm)
        print(f"wrote {path}")

if __name__ == "__main__":
    main()
