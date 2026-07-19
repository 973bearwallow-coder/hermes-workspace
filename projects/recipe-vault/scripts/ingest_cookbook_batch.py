#!/usr/bin/env python3
"""
ingest_cookbook_batch.py — Batch-ingest a multi-page cookbook OCR text dump.

DESIGNED FOR: Adobe Scan export of "Italy al Dente" by Biba Caggiano, where
  - Recipes span MULTIPLE pages
  - Each page has a PRINTED PAGE NUMBER in the footer/header
  - Exported as a single .txt with page breaks

HOW IT WORKS:
  1. Split the raw text into pages (by \f, or by a "Page N" / printed-number marker)
  2. For each page, detect if it STARTS a new recipe (has a recipe TITLE at top,
     not "continued" / "step N" / "ingredients continued")
  3. Stitch pages into recipes by page NUMBER order (not file position)
  4. Write each recipe to recipes/<slug>-cookbook.md with frontmatter
  5. Re-index the vault

USAGE:
  python3 ingest_cookbook_batch.py <book.txt> --author "Biba Caggiano" --title "Italy al Dente" [--dry-run]
  --dry-run : print the recipe boundaries it detected, write nothing (VERIFY FIRST)

INPUT FORMATS HANDLED:
  - Adobe "Page 1 of 220" footers
  - Raw "\f" form-feeds between pages
  - Printed page numbers like "— 42 —" or "42" at page top/bottom
"""
import sys, os, re, json, argparse

VAULT = "/home/tom/hermes-workspace/projects/recipe-vault"
RECIPES = os.path.join(VAULT, "recipes")

# A line that looks like a printed page number (footer/header)
PAGE_NUM_RE = re.compile(r"^\s*(?:page\s+)?(\d{1,4})\s*(?:of\s+\d{1,4})?\s*$", re.I)
ADOBE_PAGE_RE = re.compile(r"Page\s+(\d+)\s+of\s+\d+", re.I)

# Lines that mean "this page is a CONTINUATION, not a new recipe"
CONTINUATION_HINTS = [
    r"^\s*(continued|cont\.|continue)\b",
    r"^\s*\d+\.\s",          # starts mid-step-list (e.g. "3. Add the...")
    r"^\s*(ingredients?)\s*(continued|cont\.?)\b",
    r"^\s*step\s+\d+",
]
CONT_RE = [re.compile(p, re.I) for p in CONTINUATION_HINTS]

def split_pages(text):
    """Return list of (page_label, body) where page_label is printed # if found."""
    # Prefer Adobe "Page N of M" markers
    parts = re.split(ADOBE_PAGE_RE, text)
    if len(parts) > 1:
        # parts = [pre, '1', body1, '2', body2, ...]
        pages = []
        i = 1
        while i < len(parts):
            num = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ""
            pages.append((int(num), body))
            i += 2
        if pages:
            return pages
    # Fallback: form-feed
    if "\f" in text:
        raw = [p for p in text.split("\f")]
        pages = []
        for idx, chunk in enumerate(raw, 1):
            m = PAGE_NUM_RE.search(chunk.strip().splitlines()[-1]) or PAGE_NUM_RE.search(chunk.strip().splitlines()[0] if chunk.strip() else "")
            num = int(m.group(1)) if m else idx
            pages.append((num, chunk))
        return pages
    # Fallback: printed number at start/end of each blank-line-separated block
    blocks = re.split(r"\n\s*\n", text)
    pages = []
    for idx, b in enumerate(blocks, 1):
        m = PAGE_NUM_RE.search(b.strip().splitlines()[-1]) or PAGE_NUM_RE.search(b.strip().splitlines()[0] if b.strip() else "")
        num = int(m.group(1)) if m else idx
        pages.append((num, b))
    return pages

def looks_like_new_recipe(page_body):
    """Heuristic: does this page START a new recipe (title at top)?"""
    lines = [l.strip() for l in page_body.splitlines() if l.strip()]
    if not lines:
        return False, None
    # first non-page-number line
    first = None
    for l in lines:
        if PAGE_NUM_RE.match(l):
            continue
        first = l
        break
    if not first:
        return False, None
    # If first real line is a continuation hint -> not a new recipe
    for r in CONT_RE:
        if r.match(first):
            return False, None
    # Title = short-ish line (<= 80 chars), not a step, not "ingredients"
    if len(first) <= 80 and not re.match(r"^\d+\.", first) and "ingredient" not in first.lower():
        return True, first
    return False, None

def build_recipes(pages):
    """Group pages (sorted by printed number) into recipes."""
    pages_sorted = sorted(pages, key=lambda p: p[0])
    recipes = []
    cur = None
    for num, body in pages_sorted:
        is_new, title = looks_like_new_recipe(body)
        if is_new:
            if cur:
                recipes.append(cur)
            cur = {"title": title, "pages": [num], "text": body}
        else:
            if cur is None:
                # orphan continuation before any title — attach to a synthetic
                cur = {"title": f"Untitled-p{num}", "pages": [num], "text": body}
            else:
                cur["pages"].append(num)
                cur["text"] += "\n" + body
    if cur:
        recipes.append(cur)
    return recipes

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:60]

def write_recipe(rec, author, book, dry_run):
    pstart, pend = rec["pages"][0], rec["pages"][-1]
    prange = f"{pstart}" if pstart == pend else f"{pstart}-{pend}"
    slug = slugify(rec["title"])
    fm = f"# {rec['title']}\n\n**Source:** Cookbook — {book} ({author})\n**Pages:** {prange}\n\n"
    # Try to split ingredients vs instructions heuristically
    body = rec["text"]
    out = fm + body.strip() + "\n"
    if dry_run:
        return out
    path = os.path.join(RECIPES, f"{slug}-cookbook.md")
    with open(path, "w") as f:
        f.write(out)
    return path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--author", default="Biba Caggiano")
    ap.add_argument("--title", default="Italy al Dente")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    text = open(a.file, encoding="utf-8", errors="ignore").read()
    pages = split_pages(text)
    recipes = build_recipes(pages)
    print(f"Parsed {len(pages)} pages → {len(recipes)} recipes\n")
    for i, r in enumerate(recipes, 1):
        pr = r["pages"]
        prange = f"{pr[0]}" if pr[0]==pr[-1] else f"{pr[0]}-{pr[-1]}"
        print(f"  {i:3}. [{prange:>10}] {r['title']}")
    if a.dry_run:
        print("\nDRY RUN — no files written.")
        return
    os.makedirs(RECIPES, exist_ok=True)
    for r in recipes:
        p = write_recipe(r, a.author, a.title, False)
        print(f"wrote {p}")
    # re-index
    try:
        os.system(f"cd {VAULT} && /home/tom/.hermes/hermes-agent/venv/bin/python3 rebuild_ingredient_index.py")
        print("Re-indexed vault.")
    except Exception as e:
        print(f"re-index skipped: {e}")

if __name__ == "__main__":
    main()
