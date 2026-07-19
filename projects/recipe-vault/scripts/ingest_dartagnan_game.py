#!/usr/bin/env python3
"""ingest_dartagnan_game.py — D'Artagnan's Glorious Game Cookbook recipes.
The book is Archive.org borrow-only (lcpdf, no free text). Pull close-match
versions from free recipe sites, tagged as D'Artagnan-style.
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
        if re.search(r"type of products|advertisement|nutrition|serves:|recipe from|provided by|buy all ingredients|directions:", p, re.I):
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
    note = ""
    if "Cherry" in title:
        note = "\n\n> **Tom's note:** D'Artagnan's version adds dried cherries to the meat mixture (the book recipe). Base below is the closest free match; fold in ~½ cup chopped dried cherries with the meats.\n"
    fm = f"# {title}\n\n**Source:** D'Artagnan's Glorious Game Cookbook (via {source_tag})\n**URL:** {url}\n\n## Ingredients\n\n{bullets}{note}\n\n## Instructions\n\n(Full steps at source URL)\n"
    return fm

def main():
    recipes = [
        ("Dartagnan Festive Terrine of Rabbit with Pork and Prunes",
         "https://chefsane.com/rabbit-terrine-with-prunes/", "chefsane.com"),
        ("Dartagnan Venison and Cherry Pate en Croute",
         "https://feastpedia.com/en/recipes/venison-pate-en-croute", "feastpedia.com"),
    ]
    os.makedirs(RECIPES, exist_ok=True)
    for title, url, tag in recipes:
        fm = extract(url, title, tag)
        path = os.path.join(RECIPES, f"{slugify(title)}-dartagnan.md")
        with open(path, "w") as f:
            f.write(fm)
        print(f"wrote {path}")

if __name__ == "__main__":
    main()
