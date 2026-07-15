#!/usr/bin/env python3
"""
moa_report.py — Daily model newspaper + expiry watch
Run by cron each morning. Writes a markdown report and prints it (cron delivers to Telegram).
Flags:
  - models expiring within 30 days (so we pre-swap before silence)
  - new free models since last run
  - recommended current best-free mix per task type
"""
import json, os, datetime, sys

MEMORY = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEMORY, "model_catalog.json")
PREV = os.path.join(MEMORY, "model_catalog_prev.json")

def main():
    # Phase 2: refresh Artificial Analysis benchmarks before reporting so the
    # ranking reflects current real-world scores. Cheap (~2s), robust: if the
    # scrape fails it keeps the previous aa_* fields (no crash).
    try:
        import moa_benchmarks as mb
        n = mb.refresh()
        lines_bench = f"refreshed {n} benchmark rows"
    except Exception as e:
        lines_bench = f"benchmark refresh skipped ({e})"
    cat = json.load(open(CATALOG))
    models = cat["models"]
    today = datetime.date.today()
    lines = []
    lines.append(f"# 🤖 Atlas MoA Model Report — {today.isoformat()}")
    lines.append(f"_Source: OpenRouter + local Ollama · {cat['total']} models · tiers {cat['by_tier']}_\n")

    # Expiring soon
    exp = [m for m in models if m.get("expiring_soon")]
    if exp:
        lines.append("## ⚠️ Expiring Soon (auto-swap will trigger)")
        for m in sorted(exp, key=lambda x: x.get("expires_in_days") or 999):
            lines.append(f"- **{m['id']}** — {m.get('expires_in_days')}d left")
        lines.append("")
    else:
        lines.append("## ✅ No expirations in next 30 days\n")

    # New since last run
    if os.path.exists(PREV):
        prev_ids = set(m["id"] for m in json.load(open(PREV))["models"])
        new = [m for m in models if m["id"] not in prev_ids]
        if new:
            lines.append(f"## 🆕 New models ({len(new)})")
            for m in new[:15]:
                lines.append(f"- {m['id']} [{m['tier']}] q={m['quality']}")
            lines.append("")

    # Best free mix per task (quick recompute via router logic inline)
    from moa_router import load_catalog, detect_task, free_mix
    for task in ["vision_doc", "coding", "research", "chat"]:
        refs, agg = free_mix(models, task)
        refs_s = ", ".join(r["id"].split("/")[-1] for r in refs)
        lines.append(f"## 🎯 {task} — free mix")
        lines.append(f"- Refs: {refs_s}")
        lines.append(f"- Agg: {agg['id'].split('/')[-1]}\n")

    lines.append("---\n_Atlas MoA Router · cost estimates are per-task ballpark from token assumptions._")
    report = "\n".join(lines)
    # save current catalog as PREV for next run's new-model diff (copy, don't move)
    import shutil
    shutil.copyfile(CATALOG, PREV)
    return report

if __name__ == "__main__":
    # ensure catalog fresh first
    os.system("python3 " + os.path.join(os.path.dirname(__file__), "moa_catalog.py --quiet"))
    print(main())
