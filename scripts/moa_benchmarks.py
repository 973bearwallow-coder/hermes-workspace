#!/usr/bin/env python3
"""
moa_benchmarks.py — Phase 2: attach REAL third-party benchmark scores to the MoA catalog.

Scrapes the Artificial Analysis LLM leaderboard table (HTTP 200, confirmed reachable
2026-07-14) and maps each row's model name -> Artificial Analysis Intelligence Index,
Blended USD/1M tokens, Median tokens/s, Latency (first chunk). These override the
heuristic `quality` field used for ranking (heuristic remains fallback for models AA
doesn't list).

Design:
- No public JSON API (Next.js app returns HTML). We parse the rendered <table>.
- Robust: if scrape yields 0 rows, keep existing heuristic; log a warning.
- Name-matching: normalize AA model names (strip creator prefix, lowercase, collapse
  spaces) and match against catalog `id`/`name`/tags. Also keep an AA lookup dict so
  moa_router can print AA index for any picked model even without a catalog match.
- LMArena skipped (301 redirect, secondary).

USAGE:
  python3 moa_benchmarks.py            # scrape + write aa_scores.json + patch catalog
  python3 moa_benchmarks.py --quiet
Output:
  /home/tom/hermes-workspace/memory/aa_scores.json   (name -> {index,usd_1m,tok_s,latency})
  patches model_catalog.json entries with: aa_intelligence_index, aa_blended_usd_1m,
    aa_median_tok_s, aa_latency, quality_source ("aa" | "heuristic")
"""
import json, os, sys, re, datetime, argparse

MEMORY = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEMORY, "model_catalog.json")
AA_OUT = os.path.join(MEMORY, "aa_scores.json")
AA_URL = "https://artificialanalysis.ai/leaderboards/models"

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[bench] MISSING DEP: {e} — run: pip install requests beautifulsoup4")
    sys.exit(2)

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def _norm(name):
    """Normalize a model name for fuzzy matching: lowercase, drop creator prefix, collapse spaces/punct."""
    n = name.lower()
    # drop a leading 'creator/' or 'creator ' prefix
    n = re.sub(r"^[a-z0-9 ._-]+?/", "", n)
    n = re.sub(r"^[a-z0-9 ._-]+?\s+", "", n, count=1)
    n = re.sub(r"[^a-z0-9]+", " ", n).strip()
    n = re.sub(r"\s+", " ", n)
    return n

def scrape_aa():
    """Return dict raw_name -> {index, usd_1m, tok_s, latency}. Empty on failure."""
    try:
        r = requests.get(AA_URL, headers=UA, timeout=30)
    except Exception as e:
        print(f"[bench] AA fetch failed: {e}")
        return {}
    if r.status_code != 200:
        print(f"[bench] AA HTTP {r.status_code}")
        return {}
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")
    if not table:
        print("[bench] AA: no <table> found in page")
        return {}
    rows = table.find_all("tr")
    out = {}
    for row in rows[1:]:  # skip header
        cells = row.find_all("td")
        if len(cells) < 9:
            continue
        # columns (from leaderboard): Model, Context, Creator, IntelligenceIndex, Blended$/1M, MedianTok/s, Latency1st, TotalResp, ...
        raw_name = cells[0].get_text(" ", strip=True)
        def num(c):
            t = c.get_text(" ", strip=True).replace("$", "").replace(",", "")
            m = re.search(r"-?\d+(\.\d+)?", t)
            return float(m.group()) if m else None
        idx = num(cells[3]) if len(cells) > 3 else None
        usd = num(cells[4]) if len(cells) > 4 else None
        toks = num(cells[5]) if len(cells) > 5 else None
        lat = num(cells[6]) if len(cells) > 6 else None
        out[raw_name] = {"index": idx, "usd_1m": usd, "tok_s": toks, "latency": lat}
    return out

def build_match_index(aa_raw):
    """Build normalized-name -> AA record for matching against catalog."""
    idx = {}
    for raw, rec in aa_raw.items():
        idx[_norm(raw)] = rec
        # also index the bare model part (after creator) explicitly
        idx[_norm(raw.split("/")[-1] if "/" in raw else raw)] = rec
    return idx

def patch_catalog(aa_raw, quiet=False):
    data = json.load(open(CATALOG))
    models = data["models"]
    match_idx = build_match_index(aa_raw)
    hit = 0
    for m in models:
        cand_names = [_norm(m.get("id", "")), _norm(m.get("name", "") or "")]
        cand_names += [_norm(t) for t in m.get("tags", [])]
        rec = None
        for cn in cand_names:
            if cn in match_idx:
                rec = match_idx[cn]
                break
        if rec is None:
            # try partial: any AA key containing the model's short name
            short = _norm(m.get("id", "").split("/")[-1])
            short_free = _norm(m.get("id", "").split("/")[-1].replace(":free", ""))
            for k, v in match_idx.items():
                if short and short in k:
                    rec = v
                    break
            if rec is None:
                for k, v in match_idx.items():
                    if short_free and short_free in k:
                        rec = v
                        break
        if rec:
            m["aa_intelligence_index"] = rec["index"]
            m["aa_blended_usd_1m"] = rec["usd_1m"]
            m["aa_median_tok_s"] = rec["tok_s"]
            m["aa_latency"] = rec["latency"]
            m["quality"] = rec["index"] if rec["index"] is not None else m.get("quality", 5)
            m["quality_source"] = "aa"
            hit += 1
        else:
            m.setdefault("quality_source", "heuristic")
    json.dump(data, open(CATALOG, "w"), indent=1)
    json.dump(aa_raw, open(AA_OUT, "w"), indent=1)
    if not quiet:
        print(f"[bench] AA rows scraped: {len(aa_raw)} | catalog entries matched to AA: {hit}/{len(models)}")
        print(f"[bench] wrote {AA_OUT} + patched {CATALOG}")
    return hit

def refresh():
    """Scrape AA and patch the catalog. Returns # entries matched (0 on failure).
    Safe to call from cron: never raises, keeps previous aa_* fields on scrape fail."""
    try:
        aa_raw = scrape_aa()
        if not aa_raw:
            return 0
        return patch_catalog(aa_raw, quiet=True)
    except Exception:
        return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    aa_raw = scrape_aa()
    if not aa_raw:
        print("[bench] WARNING: 0 AA rows — keeping heuristic quality, no patch.")
        return
    patch_catalog(aa_raw, quiet=args.quiet)

if __name__ == "__main__":
    main()
