#!/usr/bin/env python3
"""Sparse, actionable Atlas Mission Control.

The app intentionally exposes only conversation entry points, human-readable
service state, live Kanban work, upcoming projects, and a small app registry.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from flask import Flask, Response, jsonify, render_template_string

app = Flask(__name__)

REGISTRY_FILE = Path("/home/tom/hermes-workspace/data/mission_control.json")
KANBAN_DB = Path.home() / ".hermes" / "kanban.db"
_HEALTH_CACHE: dict[str, Any] = {"at": 0.0, "apps": []}
_HEALTH_LOCK = threading.Lock()
_HEALTH_TTL_SECONDS = 15

ICONS = {
    "mic": "◉",
    "spark": "✦",
    "agents": "◎",
    "build": "◇",
}

PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#111827">
  <meta name="description" content="Talk to Atlas, see active work, upcoming projects, and open your apps.">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%23111827'/%3E%3Cpath d='M16 47 31 15h3l14 32h-8l-3-8H26l-3 8zm13-15h6l-3-8z' fill='%2369a9ff'/%3E%3C/svg%3E">
  <title>Atlas Mission Control</title>
  <style>
    :root {
      --ink: #f7f8fb; --muted: #aab2c2; --panel: rgba(27,35,51,.88);
      --panel-2: rgba(19,26,39,.82); --line: rgba(255,255,255,.09);
      --blue: #69a9ff; --blue-2: #377de3; --green: #5fd39a;
      --amber: #f2bd63; --red: #ef7a7a; --shadow: 0 18px 50px rgba(0,0,0,.24);
    }
    * { box-sizing: border-box; }
    html { background: #0b101a; }
    body {
      margin: 0; color: var(--ink); font: 16px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 15% -10%, rgba(55,125,227,.24), transparent 35rem),
        radial-gradient(circle at 95% 5%, rgba(97,79,196,.18), transparent 28rem),
        #0b101a;
      min-height: 100vh;
    }
    a { color: inherit; }
    button, a { -webkit-tap-highlight-color: transparent; }
    .shell { width: min(1120px, calc(100% - 40px)); margin: 0 auto; padding: 34px 0 62px; }
    header { display: flex; justify-content: space-between; gap: 24px; align-items: flex-start; margin-bottom: 30px; }
    .eyebrow { color: var(--blue); font-size: .73rem; letter-spacing: .15em; font-weight: 800; text-transform: uppercase; }
    h1 { margin: 7px 0 5px; font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1; letter-spacing: -.045em; }
    .subtitle { color: var(--muted); margin: 0; font-size: 1.04rem; }
    .ready { display: flex; gap: 9px; align-items: center; color: #dce7ef; background: rgba(19,26,39,.72); border: 1px solid var(--line); padding: 9px 13px; border-radius: 999px; white-space: nowrap; font-size: .88rem; }
    .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 5px rgba(95,211,154,.12); }
    .dot.attention { background: var(--amber); box-shadow: 0 0 0 5px rgba(242,189,99,.12); }
    .hero { background: linear-gradient(135deg, rgba(39,76,132,.72), rgba(24,31,48,.94)); border: 1px solid rgba(105,169,255,.26); border-radius: 26px; padding: 28px; box-shadow: var(--shadow); display: grid; grid-template-columns: 1fr auto; gap: 24px; align-items: center; }
    .hero h2 { font-size: clamp(1.55rem, 3vw, 2.2rem); letter-spacing: -.03em; margin: 0 0 8px; }
    .hero p { color: #cad5e7; margin: 0; max-width: 650px; }
    .actions { display: flex; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
    .button { display: inline-flex; min-height: 48px; align-items: center; justify-content: center; gap: 9px; padding: 0 18px; border-radius: 13px; border: 1px solid rgba(255,255,255,.12); text-decoration: none; font-weight: 760; background: rgba(255,255,255,.075); transition: transform .16s ease, background .16s ease; }
    .button.primary { color: #07111f; background: #f7f9fd; border-color: #fff; }
    .button:hover { transform: translateY(-1px); background: rgba(255,255,255,.13); }
    .button.primary:hover { background: #dfeaff; }
    section { margin-top: 30px; }
    .section-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; margin-bottom: 12px; }
    .section-head h2 { margin: 0; font-size: 1.12rem; letter-spacing: -.015em; }
    .section-head span { color: var(--muted); font-size: .82rem; }
    .grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 13px; }
    .card { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 19px; box-shadow: 0 10px 30px rgba(0,0,0,.12); }
    .card-row { display: flex; gap: 13px; align-items: flex-start; }
    .card h3 { margin: 0 0 5px; font-size: 1rem; letter-spacing: -.012em; }
    .card p { color: var(--muted); margin: 0; font-size: .9rem; }
    .badge { display: inline-flex; margin-top: 13px; color: #c8d1df; background: rgba(255,255,255,.05); border: 1px solid var(--line); border-radius: 999px; padding: 4px 9px; font-size: .73rem; font-weight: 750; }
    .priority { width: 4px; align-self: stretch; min-height: 48px; border-radius: 99px; background: var(--blue); flex: 0 0 auto; }
    .priority.blocked { background: var(--amber); }
    .empty { border: 1px dashed rgba(255,255,255,.13); color: var(--muted); background: rgba(19,26,39,.5); border-radius: 16px; padding: 18px; }
    .attention-box { border-color: rgba(242,189,99,.27); background: linear-gradient(140deg, rgba(66,49,26,.55), var(--panel-2)); }
    .apps { display: grid; grid-template-columns: repeat(4,minmax(0,1fr)); gap: 13px; }
    .app-card { position: relative; min-height: 178px; display: flex; flex-direction: column; text-decoration: none; }
    .app-card:hover { border-color: rgba(105,169,255,.38); }
    .app-top { display: flex; justify-content: space-between; gap: 12px; align-items: center; }
    .app-icon { width: 39px; height: 39px; display: grid; place-items: center; border-radius: 12px; background: rgba(105,169,255,.12); color: #a8ccff; font-size: 1.25rem; }
    .app-status { display: flex; align-items: center; gap: 7px; color: var(--muted); font-size: .73rem; font-weight: 760; }
    .app-status .dot { width: 7px; height: 7px; box-shadow: none; }
    .app-status .dot.unavailable { background: var(--red); }
    .app-card h3 { margin-top: 19px; }
    .launch { color: #bcd7ff; font-size: .8rem; font-weight: 800; margin-top: auto; padding-top: 16px; }
    .future { color: var(--muted); font-size: .84rem; margin-top: 11px; }
    footer { color: #727d90; font-size: .75rem; margin-top: 34px; text-align: center; }
    @media (max-width: 880px) { .apps { grid-template-columns: repeat(2,minmax(0,1fr)); } .hero { grid-template-columns: 1fr; } .actions { justify-content: flex-start; } }
    @media (max-width: 720px) {
      .shell { width: min(100% - 24px, 650px); padding: 22px 0 38px; }
      header { align-items: center; margin-bottom: 21px; }
      .subtitle { font-size: .92rem; }
      .ready { padding: 8px 10px; }
      .hero { border-radius: 20px; padding: 21px; gap: 19px; }
      .actions { display: grid; grid-template-columns: 1fr 1fr; }
      .button { padding: 0 12px; }
      section { margin-top: 25px; }
      .grid { grid-template-columns: 1fr; }
      .apps { grid-template-columns: 1fr; }
      .app-card { min-height: 144px; }
      .section-head span { display: none; }
    }
    @media (max-width: 410px) { .ready .label { display: none; } .actions { grid-template-columns: 1fr; } }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; } }
  </style>
</head>
<body>
<main class="shell">
  <header>
    <div><div class="eyebrow">Atlas</div><h1>Mission Control</h1><p class="subtitle">Talk. Work. Tools.</p></div>
    <div class="ready"><span class="dot {{ 'attention' if system_summary != 'Ready' else '' }}"></span><span class="label">{{ system_summary }}</span></div>
  </header>

  <section class="hero" aria-labelledby="talk-title">
    <div><div class="eyebrow">Your direct line</div><h2 id="talk-title">Talk to Atlas</h2><p>Start a voice conversation or return to Telegram. This is the quickest way to ask, decide, or approve.</p></div>
    <div class="actions">
      <a class="button primary" href="{{ contact.voice_url }}">◉ Talk now</a>
      <a class="button" href="{{ contact.telegram_url }}">Message Atlas</a>
    </div>
  </section>

  <section aria-labelledby="attention-title">
    <div class="section-head"><h2 id="attention-title">Needs Your Attention</h2><span>Only decisions or problems</span></div>
    {% if sections.attention %}<div class="grid">
      {% for task in sections.attention %}<article class="card attention-box"><div class="card-row"><span class="priority blocked"></span><div><h3>{{ task.title }}</h3><p>{{ task.detail or 'This item is waiting for a decision.' }}</p><span class="badge">Waiting on you</span></div></div></article>{% endfor %}
    </div>{% elif unavailable %}<div class="grid">
      {% for item in unavailable %}<article class="card attention-box"><div class="card-row"><span class="priority blocked"></span><div><h3>{{ item.name }} needs attention</h3><p>The app is not responding right now.</p></div></div></article>{% endfor %}
    </div>{% else %}<div class="empty">Nothing needs your attention right now.</div>{% endif %}
  </section>

  <section aria-labelledby="active-title">
    <div class="section-head"><h2 id="active-title">Active Work</h2><span>What the team is doing now</span></div>
    {% if sections.active %}<div class="grid">
      {% for task in sections.active %}<article class="card"><div class="card-row"><span class="priority"></span><div><h3>{{ task.title }}</h3><p>{{ task.detail or 'Work is currently underway.' }}</p><span class="badge">In progress</span></div></div></article>{% endfor %}
    </div>{% else %}<div class="empty">No background work is running right now.</div>{% endif %}
  </section>

  <section aria-labelledby="upcoming-title">
    <div class="section-head"><h2 id="upcoming-title">Upcoming Projects</h2><span>What is next</span></div>
    {% if sections.upcoming %}<div class="grid">
      {% for task in sections.upcoming %}<article class="card"><div class="card-row"><span class="priority {{ 'blocked' if task.status == 'blocked' else '' }}"></span><div><h3>{{ task.title }}</h3><p>{{ task.detail or 'Queued for a future work session.' }}</p><span class="badge">{{ 'Waiting' if task.status == 'blocked' else 'Up next' }}</span></div></div></article>{% endfor %}
    </div>{% else %}<div class="empty">No upcoming projects have been queued.</div>{% endif %}
  </section>

  <section aria-labelledby="apps-title">
    <div class="section-head"><h2 id="apps-title">Your Apps</h2><span>Open the tool you need</span></div>
    <div class="apps">
      {% for item in apps %}<a class="card app-card" href="{{ item.url }}">
        <div class="app-top"><span class="app-icon">{{ icons.get(item.icon, '◇') }}</span><span class="app-status"><span class="dot {{ 'unavailable' if item.status == 'unavailable' else '' }}"></span>{{ item.status_label }}</span></div>
        <h3>{{ item.name }}</h3><p>{{ item.description }}</p><span class="launch">Open app →</span>
      </a>{% endfor %}
    </div>
    <p class="future">New Atlas apps will appear here when they are ready to use.</p>
  </section>
  <footer>Private on your Tailscale network · Status refreshes automatically</footer>
</main>
<script>
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(() => {});
  setTimeout(() => location.reload(), 60000);
</script>
</body></html>"""


def _safe_web_url(value: Any) -> str:
    if not isinstance(value, str) or urlparse(value).scheme not in {"http", "https"}:
        raise ValueError("Mission Control URLs must use http or https")
    return value


def load_registry() -> dict[str, Any]:
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    contact = data.get("contact")
    apps = data.get("apps")
    if not isinstance(contact, dict) or not isinstance(apps, list):
        raise ValueError("Registry requires contact and apps")
    for key in ("voice_url", "telegram_url"):
        contact[key] = _safe_web_url(contact.get(key))
    seen: set[str] = set()
    for item in apps:
        required = ("id", "name", "description", "url")
        if not isinstance(item, dict) or not all(isinstance(item.get(k), str) and item[k].strip() for k in required):
            raise ValueError("Every app requires id, name, description, and url")
        if item["id"] in seen:
            raise ValueError(f"Duplicate app id: {item['id']}")
        seen.add(item["id"])
        item["url"] = _safe_web_url(item["url"])
        if item.get("health_url"):
            item["health_url"] = _safe_web_url(item["health_url"])
    return data


def get_tasks() -> list[dict[str, Any]]:
    if not KANBAN_DB.exists():
        return []
    try:
        db = sqlite3.connect(f"file:{KANBAN_DB}?mode=ro", uri=True, timeout=1)
        db.row_factory = sqlite3.Row
        rows = db.execute(
            "SELECT id, title, COALESCE(body, '') AS detail, status, priority, created_at "
            "FROM tasks WHERE status NOT IN ('done', 'archived', 'cancelled')"
        ).fetchall()
        db.close()
        return [dict(row) for row in rows]
    except (sqlite3.Error, OSError):
        return []


def organize_tasks(tasks: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    def order(task: dict[str, Any]) -> tuple[Any, ...]:
        return (int(task.get("priority") or 99), str(task.get("due_at") or "9999"), str(task.get("created_at") or ""))

    live = [task for task in tasks if task.get("status") not in {"done", "archived", "cancelled"}]
    active = sorted((task for task in live if task.get("status") in {"running", "in_progress"}), key=order)[:4]
    attention = sorted((task for task in live if task.get("status") == "blocked"), key=order)[:4]
    queued_states = {"ready", "todo", "triage", "scheduled", "pending"}
    upcoming_rank = {"ready": 0, "scheduled": 1, "todo": 2, "pending": 2, "triage": 3}
    upcoming = sorted(
        (task for task in live if task.get("status") in queued_states),
        key=lambda task: (upcoming_rank.get(str(task.get("status")), 9), order(task)),
    )[:6]
    return {"active": active, "attention": attention, "upcoming": upcoming}


def probe_app(item: dict[str, Any]) -> dict[str, Any]:
    result = dict(item)
    health_url = item.get("health_url")
    if not health_url:
        result.update(status="ready", status_label="Ready")
        return result
    try:
        request = urllib.request.Request(health_url, headers={"User-Agent": "Atlas-Mission-Control/1.0"})
        with urllib.request.urlopen(request, timeout=1.5) as response:
            ready = 200 <= response.status < 400
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        ready = False
    result.update(status="ready" if ready else "unavailable", status_label="Ready" if ready else "Unavailable")
    return result


def get_app_statuses(registry: dict[str, Any], force: bool = False) -> list[dict[str, Any]]:
    now = time.monotonic()
    with _HEALTH_LOCK:
        if not force and _HEALTH_CACHE["apps"] and now - float(_HEALTH_CACHE["at"]) < _HEALTH_TTL_SECONDS:
            return [dict(item) for item in _HEALTH_CACHE["apps"]]
    apps = registry["apps"]
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(apps)))) as pool:
        checked = list(pool.map(probe_app, apps))
    with _HEALTH_LOCK:
        _HEALTH_CACHE.update(at=now, apps=checked)
    return checked


def public_app(item: dict[str, Any]) -> dict[str, Any]:
    allowed = ("id", "name", "description", "url", "icon", "featured", "status", "status_label")
    return {key: item[key] for key in allowed if key in item}


def build_state() -> dict[str, Any]:
    registry = load_registry()
    apps = get_app_statuses(registry)
    sections = organize_tasks(get_tasks())
    unavailable = [item for item in apps if item.get("status") == "unavailable"]
    summary = "Ready" if not unavailable else "Needs attention"
    return {"registry": registry, "apps": apps, "sections": sections, "unavailable": unavailable, "summary": summary}


@app.get("/")
def home() -> str:
    state = build_state()
    return render_template_string(
        PAGE,
        contact=state["registry"]["contact"],
        apps=state["apps"],
        sections=state["sections"],
        unavailable=state["unavailable"],
        system_summary=state["summary"],
        icons=ICONS,
    )


@app.get("/api/status")
def status_api() -> Response:
    state = build_state()
    sections = state["sections"]
    return jsonify(
        summary=state["summary"],
        counts={key: len(sections[key]) for key in ("attention", "active", "upcoming")},
        apps=[public_app(item) for item in state["apps"]],
    )


@app.get("/health")
def health() -> Response:
    return jsonify(ok=True, service="atlas-mission-control")


@app.get("/manifest.webmanifest")
def manifest() -> Response:
    return jsonify(
        name="Atlas Mission Control",
        short_name="Mission Control",
        description="Talk to Atlas, see active work, and open your apps.",
        start_url="./",
        scope="./",
        display="standalone",
        background_color="#0b101a",
        theme_color="#111827",
    )


@app.get("/sw.js")
def service_worker() -> Response:
    script = """const CACHE='mission-control-v1';
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.add('./'))));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{if(e.request.mode==='navigate')e.respondWith(fetch(e.request).catch(()=>caches.match('./')))});
"""
    return Response(script, mimetype="application/javascript", headers={"Service-Worker-Allowed": "./"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=18787, debug=False)
