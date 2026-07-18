#!/usr/bin/env python3
"""
optimizer.py — Multi-store price comparison & savings optimizer.

Loads scraped prices from Aldi (aldi_prices.json) + Flipp (flipp_prices.json:
HT/Giant/Safeway) and computes the cheapest single-store total for a shopping
list, ranks stores by total cost, reports savings, and suggests a 2-store
hybrid ONLY if it saves > $10 vs the cheapest single stop.

Unit handling:
  - Meat keywords (pork/chicken/beef/meat/turkey/bacon/sausage/steak/ham)
    => per-lb. If a price string has "/lb", use it. Else assume per-package
    but flag as approximate.
  - Everything else => per-package (1 unit = 1 item).

Usage:
  optimizer.py --list "pork:2,rice:1,red peppers:3,eggs:12"
  optimizer.py --from-sale pork --count 5   # pulls needed items from recipe_query.py
  optimizer.py --help
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

VAULT = "/home/tom/hermes-workspace/projects/recipe-vault"
ALDI_PATH = f"{VAULT}/aldi_prices.json"
FLIPP_PATH = f"{VAULT}/flipp_prices.json"

HYBRID_THRESHOLD = 10.0  # $ savings needed to suggest a 2nd store

MEAT_KW = ["pork", "chicken", "beef", "meat", "turkey", "bacon",
           "sausage", "steak", "ham", "lamb", "veal", "fish", "shrimp",
           "ground", "ribs", "filet", "loin", "breast", "wing", "mince"]

PRICE_RE = re.compile(r"\$?\s*([\d,]+\.\d{2})")
UNIT_RE = re.compile(r"/\s*(lb|kg|ea|each|pkg|package|ct|count)", re.I)


def is_meat(name):
    n = (name or "").lower()
    return any(k in n for k in MEAT_KW)


def parse_price(raw):
    """raw may be float, '$4.39', or '$3.99/lb'. Return (value, unit)."""
    if isinstance(raw, (int, float)):
        return float(raw), "pkg"
    s = str(raw)
    m = PRICE_RE.search(s)
    if not m:
        return None, None
    val = float(m.group(1).replace(",", ""))
    um = UNIT_RE.search(s)
    unit = um.group(1).lower() if um else "pkg"
    if unit in ("ea", "each"):
        unit = "pkg"
    return val, unit


def load_stores():
    """Return dict: store_name -> list of {name, price, unit}."""
    stores = {}
    # Aldi
    try:
        d = json.load(open(ALDI_PATH))
        items = []
        for it in d.get("items", []):
            val, unit = parse_price(it.get("current_price"))
            if val is None:
                continue
            items.append({"name": it.get("name", ""), "price": val, "unit": unit})
        stores["aldi"] = items
    except Exception as e:
        print(f"[warn] aldi load failed: {e}", file=sys.stderr)

    # Flipp: HT / Giant / Safeway
    try:
        d = json.load(open(FLIPP_PATH))
        for store, items in d.get("stores", {}).items():
            norm = []
            for it in items:
                val, unit = parse_price(it.get("current_price"))
                if val is None:
                    continue
                norm.append({"name": it.get("product_name", ""), "price": val, "unit": unit})
            stores[store] = norm
    except Exception as e:
        print(f"[warn] flipp load failed: {e}", file=sys.stderr)

    return stores


def match_item(query, qty, store_items):
    """Fuzzy-match query to best store product.

    Strategy: the LAST token of the query is the core noun (e.g. 'peppers'
    in 'red peppers', 'rice' in 'white rice'). Require the core noun to appear
    as a whole word. Earlier tokens (colors like 'red') are bonuses that
    boost score but are NOT required — 'red peppers' still matches 'Green
    Peppers' because the noun 'peppers' matches.

    Meat constraint: meat queries only match meat products.
    Returns (matched_name, unit, price_for_qty) or None.
    """
    q = query.lower().strip()
    meat = is_meat(q)
    q_tokens = re.findall(r"[a-z]+", q)
    if not q_tokens:
        return None
    core = q_tokens[-1]  # noun
    modifiers = q_tokens[:-1]  # colors/adj descriptors

    best = None
    best_score = 0
    for prod in store_items:
        name = prod["name"].lower()
        p_tokens = set(re.findall(r"[a-z]+", name))
        # core noun must be a whole word in the product name
        if not re.search(r"\b" + re.escape(core) + r"\b", name):
            continue
        # meat constraint
        if meat != is_meat(name):
            continue
        # score: core match + bonus for each modifier present, penalty for extra words
        score = 1.0
        for mod in modifiers:
            if re.search(r"\b" + re.escape(mod) + r"\b", name):
                score += 0.5
        score -= 0.1 * (len(p_tokens) - len(q_tokens))
        if score > best_score:
            best_score = score
            best = prod
    if not best:
        return None
    unit = best["unit"]
    if meat and unit != "lb":
        unit = "lb"
    price_for_qty = best["price"] * qty
    return (best["name"], unit, price_for_qty)


def optimize(shopping_list):
    stores = load_stores()
    results = {}
    for store, items in stores.items():
        total = 0.0
        fulfilled = 0
        missing = []
        detail = []
        for q, qty in shopping_list:
            m = match_item(q, qty, items)
            if not m:
                missing.append(q)
                detail.append({"item": q, "matched": None, "cost": None})
                continue
            name, unit, cost = m
            total += cost
            fulfilled += 1
            detail.append({"item": q, "matched": name, "unit": unit, "cost": round(cost, 2)})
        results[store] = {
            "total": round(total, 2),
            "fulfilled": fulfilled,
            "missing": missing,
            "detail": detail,
        }

    # rank stores: prefer those fulfilling most items, then lowest total
    ranked = sorted(
        results.items(),
        key=lambda x: (x[1]["fulfilled"], -x[1]["total"]),
        reverse=True,
    )
    # only stores fulfilling ALL items are "full" candidates for cheapest_single
    full = {s: r for s, r in results.items() if not r["missing"]}
    full_ranked = sorted(full.items(), key=lambda x: x[1]["total"])

    out = {
        "list": [{"item": q, "qty": qty} for q, qty in shopping_list],
        "stores": results,
        "cheapest_single": None,
        "cheapest_total": None,
        "savings_vs_next": None,
        "hybrid": None,
        "recommendation": None,
    }

    if full_ranked:
        top_store, top = full_ranked[0]
        out["cheapest_single"] = top_store
        out["cheapest_total"] = top["total"]
        if len(full_ranked) > 1:
            next_store, nxt = full_ranked[1]
            out["savings_vs_next"] = round(nxt["total"] - top["total"], 2)
        out["recommendation"] = (
            f"Shop {top_store} only — ${top['total']:.2f}, "
            f"all {top['fulfilled']} items in stock."
        )

        # Hybrid check: min-cost cover across stores
        if len(full_ranked) > 1:
            hybrid_cost = 0.0
            hybrid_plan = {}
            for q, qty in shopping_list:
                best_store = None
                best_cost = None
                for s, r in results.items():
                    m = [d for d in r["detail"] if d["item"] == q and d["cost"] is not None]
                    if m and (best_cost is None or m[0]["cost"] < best_cost):
                        best_cost = m[0]["cost"]
                        best_store = s
                if best_store:
                    hybrid_cost += best_cost
                    hybrid_plan.setdefault(best_store, []).append(q)
            if hybrid_cost < top["total"] - HYBRID_THRESHOLD:
                out["hybrid"] = {
                    "total": round(hybrid_cost, 2),
                    "savings_vs_single": round(top["total"] - hybrid_cost, 2),
                    "plan": hybrid_plan,
                }
                out["recommendation"] += (
                    f" OR split across {len(hybrid_plan)} stores to save "
                    f"${top['total'] - hybrid_cost:.2f} (total ${hybrid_cost:.2f})."
                )
    else:
        # no store fulfills everything — recommend the one with most items
        if ranked:
            top_store, top = ranked[0]
            out["cheapest_single"] = top_store
            out["cheapest_total"] = top["total"]
            out["recommendation"] = (
                f"No store has all {len(shopping_list)} items. "
                f"Best single stop: {top_store} ({top['fulfilled']}/{len(shopping_list)} items, "
                f"${top['total']:.2f}). Missing: {', '.join(top['missing'])}."
            )

    return out


def parse_list_arg(s):
    """'pork:2,rice:1' -> [('pork',2),('rice',1)]"""
    out = []
    for part in s.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            name, qty = part.split(":", 1)
            out.append((name.strip(), float(qty.strip())))
        else:
            out.append((part, 1.0))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", help='shopping list, e.g. "pork:2,rice:1,red peppers:3"')
    ap.add_argument("--from-sale", help="ingredient to pass to recipe_query.py --sale")
    ap.add_argument("--count", type=int, default=5)
    args = ap.parse_args()

    if args.from_sale:
        import subprocess
        r = subprocess.run(
            ["/home/tom/.hermes/hermes-agent/venv/bin/python3",
             f"{VAULT}/recipe_query.py", "--sale", args.from_sale,
             "--count", str(args.count)],
            capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
            # pull ingredient names from the plan's recipes' has_ingredients
            ings = set()
            for rec in d.get("recipes", []):
                for h in rec.get("has_ingredients", []):
                    ings.add(h)
            shopping = [(i, 1.0) for i in ings]
        except Exception:
            shopping = [(args.from_sale, 1.0)]
    elif args.list:
        shopping = parse_list_arg(args.list)
    else:
        print("Provide --list or --from-sale")
        sys.exit(1)

    result = optimize(shopping)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
