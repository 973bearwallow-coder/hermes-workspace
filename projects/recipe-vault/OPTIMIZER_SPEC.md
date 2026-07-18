# Optimizer Spec — Multi-Store Price Comparison & Savings

**Purpose:** Given a shopping list (from `recipe_query.py --sale` or free-text), compute the cheapest single-store total across all scraped stores, rank stores by total cost, and report savings. Also suggest a 2-store hybrid if it clears a savings threshold.

**Inputs (data sources, all JSON):**
- `/home/tom/hermes-workspace/projects/recipe-vault/flipp_prices.json` — HT, Giant, Safeway (ZIP 22046)
- `/home/tom/hermes-workspace/projects/recipe-vault/aldi_prices.json` — Aldi FRE 69 (when Aldi bot lands)
- Future: Lidl (phase 3)

**Shopping list input:** Either
- A list of item names + qty: `[("pork", 2), ("rice", 1), ("red peppers", 3)]`
- Or piped from `recipe_query.py --sale pork --count 5` (which outputs needed ingredients)

---

## Algorithm

### Step 1 — Normalize prices
Each stored product has `current_price` (float) and possibly a unit (`/lb`, `/kg`, `/ea`, `/pkg`).
- Convert all to a **common comparator**: price per item (assume 1 unit = 1 item unless qty specified).
- If price is `$X/lb` and list says "2 lb pork" → cost = X * 2. If no unit, treat as per-item.
- Drop items with `null` price (can't compare).

### Step 2 — Fuzzy item matching
For each list item (e.g. "pork"), find the best-matching product in EACH store:
- Token overlap: "pork" → "Boneless Pork Shoulder" (score by shared tokens)
- Category awareness: if list item is a protein, prefer meat-category matches
- Pick the highest-score product per store; record its price
- If no match in a store → that store gets `None` for that item (can't fulfill)

### Step 3 — Per-store totals
For each store:
```
total = sum(matched_price[item] * qty[item] for all list items)
fulfilled = count of items with a match
```
Store is a "candidate" only if it fulfills ALL items OR we report partial fulfillment separately.

### Step 4 — Rank & report
- Sort stores by `total` ascending (only stores that fulfill all items)
- Cheapest = rank 1
- Savings vs rank 2 = rank2.total - rank1.total
- Savings vs average of all stores = avg - rank1.total
- Output:
  ```
  Cheapest single stop: Giant — $42.30
    HT: $47.10 (+$4.80)
    Safeway: $51.20 (+$8.90)
    Aldi: $39.90  ← wait, Aldi cheaper? re-rank
  → Shopping only Giant saves $X vs next best.
  ```

### Step 5 — 2-store hybrid (optional)
If splitting across 2 stores saves > `$HYBRID_THRESHOLD` (default $10) vs the cheapest single store:
- Find the min-cost cover: for each item, the cheapest store; group by store; if >1 store and savings > threshold → suggest "Giant for X,Y,Z + Safeway for A,B = $total (saves $vs single)"
- Report as an option, not a default (Tom prefers fewest stops).

---

## Output format (stdout JSON + human summary)

```json
{
  "list": [{"item": "pork", "qty": 2}, ...],
  "stores": {
    "giant": {"total": 42.30, "fulfilled": 6, "missing": []},
    "harris_teeter": {"total": 47.10, "fulfilled": 6, "missing": []},
    "safeway": {"total": 51.20, "fulfilled": 5, "missing": ["corn"]},
    "aldi": {"total": 39.90, "fulfilled": 6, "missing": []}
  },
  "cheapest_single": "aldi",
  "cheapest_total": 39.90,
  "savings_vs_next": 2.40,
  "hybrid": null,
  "recommendation": "Shop Aldi only — $39.90, saves $2.40 vs Giant, all 6 items in stock."
}
```

Human summary prints the table + recommendation line.

---

## CLI interface
```
optimizer.py --list "pork:2,rice:1,red peppers:3,eggs:12,cilantro:1,corn:2"
optimizer.py --from-sale pork --count 5   # pulls needed items from recipe_query.py
optimizer.py --help
```

## Constraints
- No external API calls — uses only local JSON (prices scraped by subbots)
- Fuzzy matching must be transparent: log which product matched each list item
- If a store has 0 matches for an item, mark `missing` and exclude from "fulfills all" ranking
- Unit normalization: per-item default; support /lb, /kg, /ea, /pkg multipliers
- Deterministic: same list + same JSON = same result

## Verification (before declaring done)
1. Run with a known list where Aldi is cheapest → confirm Aldi ranks #1
2. Run with a list where Safeway has 1 item 50% cheaper → confirm hybrid suggestion appears if >$10 savings
3. Run with an item no store has → confirm it's marked missing, not fabricated
4. Compare optimizer total vs manual sum of flipp_prices.json → must match

## Open question for Tom
- **HYBRID_THRESHOLD**: $10 savings to suggest a 2nd stop (Tom confirmed 2026-07-17: "yes I don't want to make 10 stops").
- **Unit handling**: per-package default for v1. **Meat (pork/chicken/beef/meat keywords) = per-lb** — most proteins at Aldi are $/lb not $/pkg, so weight-aware comparison matters for the exact items Tom buys most. Non-meat = per-package. Detect meat via keyword match on product name.
