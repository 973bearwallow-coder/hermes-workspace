#!/usr/bin/env python3
"""
moa_dashboard.py — Atlas MoA Router dashboard (local, Tailscale-only).

Serves a single-page view of the Mixture-of-Agents router state:
  - Task planner: pick a task -> see proposed advisers + WHY each was picked,
    estimated completion time, estimated cost, and the MoA-vs-flagship comparison.
  - Past MoA tasks: history pulled from moa_cost_log.jsonl.
  - Live catalog stats + benchmark freshness.

Local-first, no auth (Tailscale restricts access). Runs on :8770.
"""
import json, os, sys, datetime, subprocess

sys.path.insert(0, "/home/tom/.hermes/scripts")
sys.path.insert(0, "/home/tom/hermes-workspace/memory")

MEMORY = "/home/tom/hermes-workspace/memory"
CATALOG = os.path.join(MEMORY, "model_catalog.json")
AA_SCORES = os.path.join(MEMORY, "aa_scores.json")
COST_LOG = os.path.join(MEMORY, "moa_cost_log.jsonl")

from flask import Flask, render_template_string, request, jsonify

import moa_router as mr
import moa_providers as mp

app = Flask(__name__)

# ---- Flagship comparison rows (from Artificial Analysis; estimate, not A/B) ----
def load_flagships():
    rows = []
    try:
        aa = json.load(open(AA_SCORES))
    except Exception:
        aa = {}
    def grab(sub):
        for k, v in aa.items():
            if sub.lower() in k.lower():
                return k, v
        return None, None
    for label, sub in [("Claude Fable 5", "Claude Fable 5"),
                        ("GPT-5.6 Sol (high)", "GPT-5.6 Sol (high)"),
                        ("GPT-5.6 Terra (max)", "GPT-5.6 Terra (max)"),
                        ("Claude Sonnet 5 (max)", "Claude Sonnet 5 (max)")]:
        n, r = grab(sub)
        if r:
            rows.append({"label": label, "idx": r["index"], "usd": r["usd_1m"],
                         "tok_s": r["tok_s"], "latency": r["latency"]})
    return rows

TASK_TYPES = ["research", "coding", "vision_doc", "chat"]

REASON_MAP = {
    "research": "Strong reasoning / long-context model — best at synthesis, summarization, extracting determinations.",
    "coding": "Coder or reasoner model — writes/repairs code and follows spec.",
    "vision_doc": "Vision-capable model — can read images/screenshots/diagrams.",
    "chat": "General conversational model — fast, cheap, good for short replies.",
}

# rough per-call latency estimates (seconds) by provider for the aggregator
AGG_LATENCY = {
    "openrouter": 6, "local_ollama": 4, "groq": 4, "cloudflare": 5,
    "agnes": 6, "github": 7, "nvidia": 120, "mistral": 6, "openai": 8,
}

def advise_for_task(task):
    """Return refs, agg, reasons, est time, est cost — using the REAL router."""
    models = mr.load_catalog()
    refs, agg = mr.free_mix(models, task)
    up = mr.paid_upgrade(models, task)
    cost_free, _ = mr.estimate_cost(refs, agg, task)
    cost_paid, _ = mr.estimate_cost(refs, up, task) if up else (0, None)
    # est completion: use MEASURED latency if available, else fall back to rough guess.
    # refs run in PARALLEL (max of their latencies), then the aggregator runs once.
    def _lat(m):
        ms = m.get("latency_ms")
        return (ms / 1000.0) if (ms and ms > 0) else AGG_LATENCY.get(m["home_provider"], 8)
    ref_lat = max([_lat(r) for r in refs], default=4)
    agg_lat = _lat(agg)
    est_sec = ref_lat + agg_lat + 2  # parallel refs + agg + synthesis overhead
    reasons = []
    for r in refs:
        tag = []
        if "reason" in r["tags"] or r.get("modalities", {}).get("reasoning"):
            tag.append("reasoning")
        if "coder" in r["tags"]:
            tag.append("coder")
        if "longctx" in r["tags"]:
            tag.append("long-context")
        if r["home_provider"] == "local_ollama":
            tag.append("local/free/unlimited")
        reasons.append({
            "id": r["id"], "why": REASON_MAP.get(task, ""),
            "tags": ", ".join(tag) or "general", "aa": r.get("aa_intelligence_index"),
            "provider": r["home_provider"],
        })
    return {
        "task": task,
        "refs": reasons,
        "agg": {"id": agg["id"], "provider": agg["home_provider"],
                "aa": agg.get("aa_intelligence_index"), "why": "Final synthesizer — merges all adviser outputs into the answer."},
        "paid_agg": (up["id"] if up else None),
        "est_sec": est_sec,
        "cost_free": cost_free,
        "cost_paid": cost_paid,
    }

def past_tasks(limit=25):
    out = []
    try:
        lines = [l for l in open(COST_LOG) if l.strip()]
    except Exception:
        return out
    for l in lines[-limit:]:
        try:
            d = json.loads(l)
        except Exception:
            continue
        out.append({
            "ts": d.get("ts", "")[:16].replace("T", " "),
            "task": d.get("task", ""),
            "agg": d.get("agg", ""),
            "refs": ", ".join(r.split("/")[-1] for r in d.get("refs", [])),
            "cost": d.get("real_cost_agg", 0) or 0,
            "tokens": (d.get("usage", {}) or {}).get("total_tokens", 0),
        })
    return list(reversed(out))

def catalog_stats():
    try:
        cat = json.load(open(CATALOG))
    except Exception:
        return {}
    aa_hits = sum(1 for m in cat.get("models", []) if m.get("quality_source") == "aa")
    return {
        "total": cat.get("total", len(cat.get("models", []))),
        "by_tier": cat.get("by_tier", {}),
        "aa_hits": aa_hits,
        "aa_total": len(cat.get("models", [])),
    }

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas MoA Router</title>
<style>
:root{--bg:#0e1116;--card:#161b22;--ink:#e6edf3;--mut:#8b949e;--acc:#58a6ff;--grn:#3fb950;--yel:#d29922;--red:#f85149;}
*{box-sizing:border-box}body{margin:0;font:14px/1.5-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink)}
header{padding:18px 24px;border-bottom:1px solid #21262d;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:18px;margin:0}header .sub{color:var(--mut);font-size:12px}
.wrap{max-width:1100px;margin:0 auto;padding:20px 24px}
.card{background:var(--card);border:1px solid #21262d;border-radius:10px;padding:16px 18px;margin-bottom:18px}
h2{font-size:15px;margin:0 0 12px;color:var(--acc);letter-spacing:.3px}
.row{display:flex;gap:18px;flex-wrap:wrap}
.kpi{flex:1;min-width:140px;background:#0d1117;border:1px solid #21262d;border-radius:8px;padding:12px}
.kpi .n{font-size:22px;font-weight:700}.kpi .l{color:var(--mut);font-size:11px;text-transform:uppercase}
form{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
select,input,button{background:#0d1117;color:var(--ink);border:1px solid #30363d;border-radius:7px;padding:9px 12px;font-size:14px}
button{background:var(--acc);color:#04101f;border:0;font-weight:600;cursor:pointer}
button:hover{filter:brightness(1.1)}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #21262d;vertical-align:top}
th{color:var(--mut);font-weight:600;font-size:11px;text-transform:uppercase}
.tag{display:inline-block;background:#21262d;border-radius:5px;padding:1px 7px;margin:1px;font-size:11px;color:var(--mut)}
.reason{color:var(--mut);font-size:12px;max-width:420px}
.cmp td:first-child{font-weight:600}
.us{color:var(--grn)}.flag{color:var(--acc)}
.pill{font-size:11px;padding:2px 8px;border-radius:20px;background:#21262d;color:var(--mut)}
.note{color:var(--mut);font-size:12px;font-style:italic}
a{color:var(--acc);text-decoration:none}
</style></head><body>
<header><h1>🤖 Atlas MoA Router</h1><div class="sub">local-first · free/cheap models · benchmark-driven</div></header>
<div class="wrap">

<div class="card"><h2>Live Catalog</h2><div class="row">
<div class="kpi"><div class="n">{{stats.total}}</div><div class="l">Models</div></div>
<div class="kpi"><div class="n">{{stats.by_tier.get('free',0)}}</div><div class="l">Free</div></div>
<div class="kpi"><div class="n">{{stats.by_tier.get('cheap',0)}}</div><div class="l">Cheap</div></div>
<div class="kpi"><div class="n">{{stats.aa_hits}}</div><div class="l">Benchmarked (AA)</div></div>
</div></div>

<div class="card"><h2>Plan a Task</h2>
<form method="get">
<label>Task type<select name="task">{% for t in tasks %}<option value="{{t}}" {% if t==cur %}selected{%endif%}>{{t}}</option>{% endfor %}</select></label>
<label>Or describe it<input name="desc" placeholder="e.g. summarize this transcript" size="34"></label>
<button>Plan →</button>
</form>
{% if plan %}
<div class="row" style="margin-top:16px">
<div class="kpi"><div class="n">{{plan.est_sec}}s</div><div class="l">Est. completion</div></div>
<div class="kpi"><div class="n us">${{'%.5f'|format(plan.cost_free)}}</div><div class="l">Free cost / task</div></div>
<div class="kpi"><div class="n">${{'%.5f'|format(plan.cost_paid) if plan.cost_paid else '—'}}</div><div class="l">Cheap-paid / task</div></div>
</div>

<h2 style="margin-top:18px">Proposed Advisers (references, run in parallel)</h2>
<table><tr><th>Model</th><th>Provider</th><th>AA Idx</th><th>Role</th><th>Why picked</th></tr>
{% for r in plan.refs %}<tr>
<td><code>{{r.id}}</code></td><td><span class="pill">{{r.provider}}</span></td>
<td>{{r.aa if r.aa else '—'}}</td>
<td>{% for t in r.tags.split(', ') %}<span class="tag">{{t}}</span>{% endfor %}</td>
<td class="reason">{{r.why}}</td></tr>{% endfor %}
<tr><td colspan="5" style="border:0;color:var(--mut);font-size:12px">→ Aggregator: <code>{{plan.agg.id}}</code> ({{plan.agg.provider}}) — {{plan.agg.why}}{% if plan.paid_agg %} · cheap-paid alt: <code>{{plan.paid_agg}}</code>{% endif %}</td></tr>
</table>

<h2 style="margin-top:18px">MoA vs Flagship (benchmark estimate*)</h2>
<table class="cmp"><tr><th>Model</th><th>AA Idx</th><th>$/1M</th><th>tok/s</th></tr>
<tr class="us"><td>OUR Free MoA ({{plan.agg.id.split('/')[-1]}})</td><td>{{plan.agg.aa if plan.agg.aa else '—'}}</td><td>$0.00</td><td>—</td></tr>
{% if plan.paid_agg %}<tr><td>OUR Cheap-Paid ({{plan.paid_agg.split('/')[-1]}})</td><td>~44</td><td>$0.18</td><td>—</td></tr>{% endif %}
{% for f in flagships %}<tr class="flag"><td>{{f.label}}</td><td>{{f.idx}}</td><td>${{f.usd}}</td><td>{{f.tok_s}}</td></tr>{% endfor %}
</table>
<p class="note">*Quality indices from Artificial Analysis independent benchmarking. We cannot execute GPT/Claude (no keys) so this is an estimate, not a blind A/B. Cost gap is 40–4000× in our favor.</p>
{% endif %}
</div>

<div class="card"><h2>Past MoA Tasks</h2>
{% if history %}<table><tr><th>When</th><th>Task</th><th>Aggregator</th><th>Advisers</th><th>Tokens</th><th>Cost</th></tr>
{% for h in history %}<tr><td>{{h.ts}}</td><td>{{h.task}}</td><td><code>{{h.agg.split('/')[-1]}}</code></td><td class="reason">{{h.refs}}</td><td>{{h.tokens}}</td><td class="us">${{'%.4f'|format(h.cost)}}</td></tr>{% endfor %}
</table>{% else %}<p class="note">No tasks run yet. Execute one with: <code>python3 moa_exec.py "your task. Transcript: /path/to.txt"</code></p>{% endif %}
</div>

<p class="note">Tailscale-only · Charles (100.115.214.128) · generated {{now}}</p>
</div></body></html>"""

@app.route("/")
def index():
    task = request.args.get("task", "")
    desc = request.args.get("desc", "").strip()
    plan = None
    if desc:
        task = mr.detect_task(desc)
    if task in TASK_TYPES:
        plan = advise_for_task(task)
    return render_template_string(PAGE,
        stats=catalog_stats(), tasks=TASK_TYPES, cur=task, plan=plan,
        flagships=load_flagships(), history=past_tasks(), now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/api/plan")
def api_plan():
    desc = request.args.get("desc", "")
    task = mr.detect_task(desc) if desc else request.args.get("task", "research")
    return jsonify(advise_for_task(task))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8770, debug=False)
