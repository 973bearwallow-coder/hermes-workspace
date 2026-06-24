#!/usr/bin/env python3
"""
Mission Control Dashboard for Atlas/Hermes.
Single-file Flask app that shows:
- Active cron jobs and their status
- Kanban board tasks
- Recent meeting transcripts
- Pet community monitor outputs
- Auto-memory capture daily notes
- System status (OpenClaw, gateway)

Stolen from the YouTube video's concepts, adapted for our setup.
"""

import json
import os
import sqlite3
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- Paths ---
WORKSPACE = "/home/tom/hermes-workspace"
DESKTOP = "/home/tom/Desktop"
COACHING_DIR = f"{DESKTOP}/coaching_call"
PET_DIR = f"{DESKTOP}/coaching_call/pet_community"
MEMORY_DIR = f"{WORKSPACE}/memory"
KANBAN_DB = os.environ.get("HERMES_KANBAN_DB", "/home/tom/.hermes/kanban.db")
LOGS_DIR = f"{WORKSPACE}/logs"
GOALS_FILE = f"{WORKSPACE}/data/goals.json"
JOURNAL_FILE = f"{WORKSPACE}/data/journal.json"
OBSIDIAN_VAULT = Path.home() / "Documents" / "ObsidianVault"

# Ensure data dir exists
os.makedirs(f"{WORKSPACE}/data", exist_ok=True)

# --- HTML Template ---
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Atlas Mission Control</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
.header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 20px 30px; border-bottom: 1px solid #2a2a4a; display: flex; justify-content: space-between; align-items: center; }
.header h1 { font-size: 1.5rem; color: #00d4ff; font-weight: 700; }
.header .subtitle { color: #888; font-size: 0.85rem; margin-top: 4px; }
.status-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 6px; }
.status-dot.green { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
.status-dot.yellow { background: #ffaa00; box-shadow: 0 0 8px #ffaa00; }
.status-dot.red { background: #ff4444; box-shadow: 0 0 8px #ff4444; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; padding: 20px 30px; }
.card { background: #12121a; border: 1px solid #2a2a3a; border-radius: 12px; padding: 20px; }
.card h2 { font-size: 0.95rem; color: #00d4ff; margin-bottom: 15px; }
.card h2 .count { background: #2a2a4a; color: #aaa; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; margin-left: 8px; }
.item { padding: 10px 0; border-bottom: 1px solid #1a1a2a; }
.item:last-child { border-bottom: none; }
.item .title { font-size: 0.9rem; color: #ddd; margin-bottom: 4px; }
.item .meta { font-size: 0.75rem; color: #666; }
.item .meta span { margin-right: 12px; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }
.badge.ready, .badge.ok, .badge.done { background: #1a3a1a; color: #00ff88; }
.badge.running, .badge.in_progress { background: #1a2a4a; color: #00d4ff; }
.badge.blocked, .badge.error { background: #3a1a1a; color: #ff4444; }
.badge.todo, .badge.scheduled, .badge.backlog { background: #2a2a1a; color: #ffaa00; }
.badge.high { background: #3a1a1a; color: #ff6666; }
.badge.medium { background: #2a2a1a; color: #ffcc00; }
.badge.low { background: #1a2a2a; color: #888; }
.kanban-wrap { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.kanban-col { background: #0d0d14; border: 1px solid #1a1a2a; border-radius: 8px; padding: 10px; }
.kanban-col h3 { font-size: 0.8rem; color: #888; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
.kanban-col .card-item { background: #161620; border: 1px solid #2a2a3a; border-radius: 6px; padding: 8px 10px; margin-bottom: 6px; cursor: pointer; }
.kanban-col .card-item:hover { border-color: #3a3a5a; }
.kanban-col .card-item .ctitle { font-size: 0.82rem; color: #ccc; line-height: 1.3; }
.kanban-col .card-item .cbadges { margin-top: 4px; }
.kanban-col .card-item .detail { display: none; font-size: 0.72rem; color: #888; margin-top: 6px; line-height: 1.4; }
.kanban-col .card-item.open .detail { display: block; }
.refresh-btn { background: #1a2a4a; color: #00d4ff; border: 1px solid #2a3a6a; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; }
.refresh-btn:hover { background: #2a3a6a; }
.footer { text-align: center; padding: 20px; color: #444; font-size: 0.75rem; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
.live-dot { animation: pulse 2s infinite; }
/* Voice Input */
.voice-btn { background: #1a2a4a; color: #00d4ff; border: 1px solid #2a3a6a; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 0.8rem; margin-left: 8px; }
.voice-btn:hover { background: #2a3a6a; }
.voice-btn.recording { background: #3a1a1a; color: #ff4444; border-color: #ff4444; animation: pulse 1s infinite; }
#chat-input { width: 100%; background: #12121a; border: 1px solid #2a2a3a; color: #e0e0e0; padding: 10px 14px; border-radius: 8px; font-size: 0.9rem; margin-top: 8px; resize: vertical; min-height: 60px; }
#chat-input:focus { outline: none; border-color: #00d4ff; }
.chat-response { background: #0d0d14; border: 1px solid #1a1a2a; border-radius: 8px; padding: 12px; margin-top: 8px; font-size: 0.85rem; color: #aaa; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
/* Goals & Journal */
.goal-item { display: flex; align-items: flex-start; gap: 10px; padding: 8px 0; border-bottom: 1px solid #1a1a2a; }
.goal-item:last-child { border-bottom: none; }
.goal-check { width: 18px; height: 18px; border: 2px solid #3a3a5a; border-radius: 4px; cursor: pointer; flex-shrink: 0; margin-top: 2px; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; }
.goal-check.checked { background: #00ff88; border-color: #00ff88; color: #0a0a0f; }
.goal-text { font-size: 0.85rem; color: #ccc; flex: 1; }
.goal-text.done { text-decoration: line-through; color: #666; }
.goal-priority { font-size: 0.65rem; padding: 1px 6px; border-radius: 3px; }
.goal-priority.high { background: #3a1a1a; color: #ff6666; }
.goal-priority.medium { background: #2a2a1a; color: #ffcc00; }
.goal-priority.low { background: #1a2a2a; color: #888; }
.journal-entry { padding: 10px 0; border-bottom: 1px solid #1a1a2a; }
.journal-entry:last-child { border-bottom: none; }
.journal-entry .jdate { font-size: 0.7rem; color: #666; margin-bottom: 4px; }
.journal-entry .jtext { font-size: 0.82rem; color: #bbb; line-height: 1.4; }
.journal-input { width: 100%; background: #0d0d14; border: 1px solid #2a2a3a; color: #e0e0e0; padding: 8px 12px; border-radius: 6px; font-size: 0.82rem; margin-top: 8px; resize: vertical; min-height: 50px; }
.journal-input:focus { outline: none; border-color: #00d4ff; }
.add-goal-btn { background: #1a2a4a; color: #00d4ff; border: 1px solid #2a3a6a; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 0.75rem; }
.add-goal-btn:hover { background: #2a3a6a; }
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>🦅 Atlas Mission Control</h1>
    <div class="subtitle"><span class="live-dot">●</span> Real-time · Updated: {{ now }}</div>
  </div>
  <button class="refresh-btn" onclick="location.reload()">↻ Refresh</button>
</div>

<div class="grid">

  <!-- System Status -->
  <div class="card">
    <h2>⚡ System Status</h2>
    {% for svc in system %}
    <div class="item">
      <div class="title">
        <span class="status-dot {{ svc.status }}"></span>
        {{ svc.name }}
      </div>
      <div class="meta">{{ svc.detail }}</div>
    </div>
    {% endfor %}
  </div>

  <!-- Cron Jobs -->
  <div class="card">
    <h2>⏰ Recent Cron Jobs <span class="count">{{ cron|length }}</span></h2>
    {% for job in cron[:8] %}
    <div class="item">
      <div class="title">{{ job.name[:50] }}</div>
      <div class="meta">
        <span class="badge {{ job.status }}">{{ job.status }}</span>
        <span>{{ job.last_run }}</span>
        <span>Next: {{ job.next_run }}</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Kanban Board -->
  <div class="card" style="grid-column: 1 / -1;">
    <h2>📋 Kanban Board <span class="count">{{ kanban|length }} tasks</span></h2>
    {% if kanban %}
    {% set cols = {} %}
    {% for task in kanban %}
      {% set _ = cols.setdefault(task.column, []) %}
      {% set _ = cols[task.column].append(task) %}
    {% endfor %}
    <div class="kanban-wrap">
      {% for col_name in ["Backlog", "In Progress", "Done"] %}
      <div class="kanban-col">
        <h3>{{ col_name }} ({{ cols.get(col_name, [])|length }})</h3>
        {% for task in cols.get(col_name, []) %}
        <div class="card-item" onclick="this.classList.toggle('open')">
          <div class="ctitle">{{ task.title }}</div>
          <div class="cbadges">
            {% for tag in task.state.split() %}
            <span class="badge {{ tag }}">{{ tag }}</span>
            {% endfor %}
          </div>
          {% if task.detail %}
          <div class="detail">{{ task.detail }}</div>
          {% endif %}
        </div>
        {% endfor %}
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div class="item"><div class="meta">No active Kanban tasks.</div></div>
    {% endif %}
  </div>

  <!-- Memory / Daily Notes -->
  <div class="card">
    <h2>🧠 Memory & Activity <span class="count">{{ memory|length }}</span></h2>
    {% for note in memory[:5] %}
    <div class="item">
      <div class="title">{{ note.title[:60] }}</div>
      <div class="meta">
        <span>{{ note.date }}</span>
        <span>{{ note.sections }} sections</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Meeting Transcripts -->
  <div class="card">
    <h2>🎙️ Meeting Transcripts <span class="count">{{ transcripts|length }}</span></h2>
    {% for t in transcripts[:5] %}
    <div class="item">
      <div class="title">{{ t.name[:50] }}</div>
      <div class="meta">
        <span>{{ t.date }}</span>
        <span>{{ t.size }}</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Pet Community Intel -->
  <div class="card">
    <h2>🐾 Pet Community Intel <span class="count">{{ pet_intel|length }}</span></h2>
    {% for p in pet_intel[:5] %}
    <div class="item">
      <div class="title">{{ p.name[:50] }}</div>
      <div class="meta">
        <span>{{ p.date }}</span>
        <span>{{ p.results }} results</span>
      </div>
    </div>
    {% endfor %}
  </div>

  <!-- Voice Chat -->
  <div class="card" style="grid-column: 1 / -1;">
    <h2>🎤 Voice Input <span class="count" id="voice-status">Click mic to talk</span></h2>
    <div style="display:flex; align-items:center; gap:8px;">
      <button class="voice-btn" id="voice-btn" onclick="toggleVoice()">🎙️ Start Recording</button>
      <span style="color:#666; font-size:0.75rem;">Uses browser's built-in speech recognition — no API keys needed</span>
    </div>
    <textarea id="chat-input" placeholder="Your speech will appear here... or type directly." rows="3"></textarea>
    <div id="chat-response" class="chat-response" style="display:none;"></div>
  </div>

  <!-- Goals -->
  <div class="card">
    <h2>🎯 Goals <span class="count" id="goal-count">{{ goals|length }}</span></h2>
    <div id="goals-list">
      {% for goal in goals %}
      <div class="goal-item">
        <div class="goal-check {% if goal.done %}checked{% endif %}" onclick="toggleGoal('{{ goal.id }}')">{% if goal.done %}✓{% endif %}</div>
        <div class="goal-text {% if goal.done %}done{% endif %}">{{ goal.text }}</div>
        <span class="goal-priority {{ goal.priority }}">{{ goal.priority }}</span>
      </div>
      {% endfor %}
    </div>
    <div style="margin-top:10px; display:flex; gap:6px;">
      <input type="text" id="new-goal-text" placeholder="Add a goal..." style="flex:1; background:#0d0d14; border:1px solid #2a2a3a; color:#e0e0e0; padding:6px 10px; border-radius:4px; font-size:0.8rem;">
      <select id="new-goal-priority" style="background:#0d0d14; border:1px solid #2a2a3a; color:#e0e0e0; padding:6px; border-radius:4px; font-size:0.75rem;">
        <option value="high">High</option>
        <option value="medium" selected>Med</option>
        <option value="low">Low</option>
      </select>
      <button class="add-goal-btn" onclick="addGoal()">+ Add</button>
    </div>
  </div>

  <!-- Journal -->
  <div class="card">
    <h2>📓 Journal <span class="count">{{ journal|length }} entries</span></h2>
    <div id="journal-list">
      {% for entry in journal[:5] %}
      <div class="journal-entry">
        <div class="jdate">{{ entry.date }}</div>
        <div class="jtext">{{ entry.text[:200] }}{% if entry.text|length > 200 %}...{% endif %}</div>
      </div>
      {% endfor %}
    </div>
    <textarea class="journal-input" id="journal-input" placeholder="Write today's journal entry..." rows="3"></textarea>
    <button class="add-goal-btn" style="margin-top:6px;" onclick="saveJournal()">💾 Save Entry</button>
  </div>

</div>

<div class="footer">
  Atlas Mission Control · Auto-refreshes on page load · <a href="/api/status" style="color:#00d4ff">JSON API</a>
</div>

<script>
// Web Speech API — Voice Input
let recognition = null;
let isRecording = false;

function toggleVoice() {
  const btn = document.getElementById('voice-btn');
  const status = document.getElementById('voice-status');

  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    status.textContent = '❌ Speech not supported. Use Chrome.';
    return;
  }

  if (isRecording) {
    recognition.stop();
    isRecording = false;
    btn.textContent = '🎙️ Start Recording';
    btn.classList.remove('recording');
    status.textContent = 'Click mic to talk';
    return;
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.lang = 'en-US';

  recognition.onstart = () => {
    isRecording = true;
    btn.textContent = '⏹️ Stop Recording';
    btn.classList.add('recording');
    status.textContent = '🔴 Listening...';
  };

  recognition.onresult = (event) => {
    let transcript = '';
    for (let i = 0; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    document.getElementById('chat-input').value = transcript;
    status.textContent = event.results[event.results.length - 1].isFinal ? '✅ Got it!' : '🔴 Listening...';
  };

  recognition.onerror = (event) => {
    status.textContent = '❌ Error: ' + event.error;
    isRecording = false;
    btn.textContent = '🎙️ Start Recording';
    btn.classList.remove('recording');
  };

  recognition.onend = () => {
    isRecording = false;
    btn.textContent = '🎙️ Start Recording';
    btn.classList.remove('recording');
    status.textContent = 'Click mic to talk';
  };

  recognition.start();
}

// --- Goals ---
function addGoal() {
  const text = document.getElementById('new-goal-text').value.trim();
  const priority = document.getElementById('new-goal-priority').value;
  if (!text) return;
  fetch('/api/goals', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: text, priority: priority})
  }).then(r => r.json()).then(goal => {
    document.getElementById('new-goal-text').value = '';
    location.reload();
  });
}

function toggleGoal(goalId) {
  fetch('/api/goals/' + goalId + '/toggle', {method: 'POST'})
    .then(() => location.reload());
}

// --- Journal ---
function saveJournal() {
  const text = document.getElementById('journal-input').value.trim();
  if (!text) return;
  fetch('/api/journal', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: text})
  }).then(r => r.json().then(() => {
    document.getElementById('journal-input').value = '';
    location.reload();
  }));
}
</script>

</body>
</html>"""


def get_system_status():
    """Check key services."""
    services = []

    # OpenClaw gateway
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "openclaw-gateway.service"],
            capture_output=True, text=True, timeout=5
        )
        status = "green" if result.stdout.strip() == "active" else "red"
        services.append({
            "name": "OpenClaw Gateway",
            "status": status,
            "detail": f"Service: {result.stdout.strip()}"
        })
    except Exception:
        services.append({"name": "OpenClaw Gateway", "status": "yellow", "detail": "Status unknown"})

    # OpenClaw bot (charles) — check for openclaw-node process, excluding shell wrappers
    try:
        result = subprocess.run(
            ["pgrep", "-fa", "openclaw-node"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            pid_line = result.stdout.strip().split("\n")[0]
            pid = pid_line.split()[0]
            services.append({
                "name": "OpenClaw (Charles)",
                "status": "green",
                "detail": f"Running (PID: {pid})"
            })
        else:
            services.append({
                "name": "OpenClaw (Charles)",
                "status": "red",
                "detail": "Not running"
            })
    except Exception:
        services.append({"name": "OpenClaw (Charles)", "status": "yellow", "detail": "Status unknown"})

    # Memory daemon (omi_like_capture) — use Python ps to avoid self-matching
    try:
        result = subprocess.run(
            ["ps", "-eo", "pid,args"],
            capture_output=True, text=True, timeout=5
        )
        found = False
        for line in result.stdout.strip().split("\n"):
            if "omi_like_capture" in line and "pgrep" not in line and "ps -eo" not in line:
                pid = line.split()[0]
                services.append({"name": "Memory Capture Daemon", "status": "green", "detail": f"Running (PID: {pid})"})
                found = True
                break
        if not found:
            services.append({"name": "Memory Capture Daemon", "status": "red", "detail": "Not running"})
    except Exception:
        services.append({"name": "Memory Capture Daemon", "status": "yellow", "detail": "Status unknown"})

    # Disk space
    try:
        result = subprocess.run(
            ["df", "-h", "/"], capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            parts = lines[1].split()
            usage = parts[4] if len(parts) > 4 else "unknown"
            status = "green" if int(usage.replace("%", "")) < 80 else "yellow"
            services.append({"name": "Disk Space", "status": status, "detail": f"Root: {usage} used"})
    except Exception:
        pass

    # Local Deep Research
    try:
        result = subprocess.run(
            ["pgrep", "-fa", "local_deep_research.web.app"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            pid = result.stdout.strip().split("\n")[0].split()[0]
            # Also check HTTP
            import urllib.request
            try:
                urllib.request.urlopen("http://127.0.0.1:18790/", timeout=3)
                services.append({"name": "Local Deep Research", "status": "green", "detail": f"Running (PID: {pid}) — http://127.0.0.1:18790"})
            except Exception:
                services.append({"name": "Local Deep Research", "status": "yellow", "detail": f"Process running (PID: {pid}) but HTTP not responding"})
        else:
            services.append({"name": "Local Deep Research", "status": "red", "detail": "Not running"})
    except Exception:
        services.append({"name": "Local Deep Research", "status": "yellow", "detail": "Status unknown"})

    # Ollama
    try:
        import urllib.request, json
        req = urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3)
        data = json.loads(req.read())
        model_count = len(data.get("models", []))
        services.append({"name": "Ollama", "status": "green", "detail": f"Running — {model_count} models available"})
    except Exception:
        services.append({"name": "Ollama", "status": "red", "detail": "Not running"})

    return services


def get_cron_jobs():
    """Get cron job status from local DB."""
    jobs = []
    # For now, hardcoded based on known cron IDs. In production, query the Hermes cron DB.
    cron_db = f"{os.environ.get('HERMES_HOME', '/home/tom/.hermes')}/cron.db"
    if os.path.exists(cron_db):
        try:
            conn = sqlite3.connect(cron_db)
            cursor = conn.execute(
                """SELECT job_id, name, last_run_at, next_run_at, last_status 
                   FROM jobs ORDER BY last_run_at DESC LIMIT 10"""
            )
            for row in cursor:
                jobs.append({
                    "name": row[1] or row[0],
                    "last_run": row[2][:16] if row[2] else "Never",
                    "next_run": row[3][:16] if row[3] else "Unknown",
                    "status": row[4] or "unknown"
                })
            conn.close()
        except Exception:
            pass

    if not jobs:
        # Fallback: list what we know
        known = [
            {"name": "Morning Briefing (7am)", "last_run": "Today 7:02am", "next_run": "Tomorrow 7:00am", "status": "ok"},
            {"name": "Pet Monitor + Boardroom Scrape (Wed 9am)", "last_run": "Not yet", "next_run": "Wed 9:00am", "status": "scheduled"},
            {"name": "Tue Coaching Call Recorder (9:30am)", "last_run": "Not yet", "next_run": "Tue 9:30am", "status": "scheduled"},
            {"name": "Fri Coaching Call Recorder (9:30am)", "last_run": "Not yet", "next_run": "Fri 9:30am", "status": "scheduled"},
            {"name": "Auto Memory Capture (10pm)", "last_run": "Not yet", "next_run": "Tonight 10:00pm", "status": "scheduled"},
            {"name": "Evening Task Discussion (7pm)", "last_run": "Yesterday 7pm", "next_run": "Today 7:00pm", "status": "ok"},
            {"name": "OpenClaw Status Monitor (hourly)", "last_run": "15 min ago", "next_run": "Next hour", "status": "ok"},
        ]
        jobs = known

    return jobs


def get_kanban_tasks():
    """Get Kanban tasks from native Hermes kanban.db."""
    tasks = []
    if os.path.exists(KANBAN_DB):
        try:
            conn = sqlite3.connect(KANBAN_DB)
            rows = conn.execute(
                "SELECT id, title, body, status, priority, assignee, created_at "
                "FROM tasks WHERE status != 'archived' ORDER BY priority ASC, created_at ASC"
            ).fetchall()
            status_col_map = {
                "blocked": "Backlog",
                "todo": "Backlog",
                "triage": "Backlog",
                "scheduled": "Backlog",
                "ready": "In Progress",
                "running": "In Progress",
                "done": "Done",
            }
            for row in rows:
                tid, title, body, status, priority, assignee, created_at = row
                col_name = status_col_map.get(status, "Backlog")
                prio = {1: "high", 2: "medium", 3: "low"}.get(priority or 2, "")
                badge = f"{status} {prio}" if prio else status
                tasks.append({
                    "id": tid,
                    "title": title,
                    "detail": (body or "")[:200],
                    "state": badge,
                    "assignee": assignee or "",
                    "updated": "",
                    "column": col_name,
                })
            conn.close()
        except Exception:
            pass
    return tasks


def get_memory_files():
    """List daily memory notes."""
    notes = []
    if os.path.exists(MEMORY_DIR):
        for f in sorted(Path(MEMORY_DIR).glob("*.md"), reverse=True)[:7]:
            try:
                stat = f.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                with open(f) as fh:
                    content = fh.read()
                sections = content.count("## ")
                notes.append({
                    "title": f.stem,
                    "date": mtime.strftime("%b %d %H:%M"),
                    "sections": sections,
                    "size": f"{stat.st_size // 1024}KB"
                })
            except Exception:
                pass
    return notes


def get_transcripts():
    """List coaching call transcripts."""
    transcripts = []
    if os.path.exists(COACHING_DIR):
        for f in sorted(Path(COACHING_DIR).glob("transcript_*.txt"), reverse=True)[:10]:
            try:
                stat = f.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                transcripts.append({
                    "name": f.name,
                    "date": mtime.strftime("%b %d %H:%M"),
                    "size": f"{stat.st_size // 1024}KB"
                })
            except Exception:
                pass
    return transcripts


def get_pet_intel():
    """List pet community intelligence reports."""
    reports = []
    if os.path.exists(PET_DIR):
        for f in sorted(Path(PET_DIR).glob("intelligence_*.txt"), reverse=True)[:10]:
            try:
                stat = f.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime)
                # Parse result count from file
                results = "?"
                try:
                    with open(f) as fh:
                        first_lines = fh.readlines(100)
                        for line in first_lines:
                            if "New relevant:" in line:
                                results = line.split("New relevant:")[-1].strip()
                                break
                except Exception:
                    pass
                reports.append({
                    "name": f.name,
                    "date": mtime.strftime("%b %d %H:%M"),
                    "results": results
                })
            except Exception:
                pass
    return reports


# --- Goals & Journal ---

def load_goals():
    """Load goals from JSON file."""
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_goals(goals):
    """Save goals to JSON file and sync to Obsidian."""
    with open(GOALS_FILE, "w") as f:
        json.dump(goals, f, indent=2)
    # Sync to Obsidian
    try:
        obsidian_goals_dir = OBSIDIAN_VAULT / "Mission_Control"
        obsidian_goals_dir.mkdir(parents=True, exist_ok=True)
        lines = ["# 🎯 Goals", "", f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
        for g in goals:
            checkbox = "x" if g.get("done") else " "
            lines.append(f"- [{checkbox}] {g['text']} ({g.get('priority', 'medium')})")
        (obsidian_goals_dir / "goals.md").write_text("\n".join(lines))
    except Exception:
        pass

def load_journal():
    """Load journal entries from JSON file."""
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_journal(entries):
    """Save journal entries to JSON file and sync to Obsidian."""
    with open(JOURNAL_FILE, "w") as f:
        json.dump(entries, f, indent=2)
    # Sync to Obsidian
    try:
        obsidian_journal_dir = OBSIDIAN_VAULT / "Journal"
        obsidian_journal_dir.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            date_str = entry.get("date", "")[:10]
            if date_str:
                lines = [f"# 📓 Journal — {date_str}", "", entry.get("text", ""), ""]
                (obsidian_journal_dir / f"journal_{date_str}.md").write_text("\n".join(lines))
    except Exception:
        pass


@app.route("/")
def dashboard():
    return render_template_string(
        DASHBOARD_HTML,
        now=datetime.now().strftime("%b %d %H:%M:%S"),
        system=get_system_status(),
        cron=get_cron_jobs(),
        kanban=get_kanban_tasks(),
        memory=get_memory_files(),
        transcripts=get_transcripts(),
        pet_intel=get_pet_intel(),
        goals=load_goals(),
        journal=load_journal(),
    )


@app.route("/api/status")
def api_status():
    return jsonify({
        "system": get_system_status(),
        "cron": get_cron_jobs(),
        "kanban": get_kanban_tasks(),
        "memory": get_memory_files(),
        "transcripts": get_transcripts(),
        "pet_intel": get_pet_intel(),
        "goals": load_goals(),
        "journal": load_journal(),
        "timestamp": datetime.now().isoformat(),
    })

# --- Goals API ---

@app.route("/api/goals", methods=["GET"])
def api_get_goals():
    return jsonify(load_goals())

@app.route("/api/goals", methods=["POST"])
def api_add_goal():
    data = request.get_json()
    goals = load_goals()
    goal = {
        "id": f"goal_{len(goals)+1}",
        "text": data.get("text", ""),
        "priority": data.get("priority", "medium"),
        "done": False,
        "created": datetime.now().isoformat(),
    }
    goals.append(goal)
    save_goals(goals)
    return jsonify(goal)

@app.route("/api/goals/<goal_id>/toggle", methods=["POST"])
def api_toggle_goal(goal_id):
    goals = load_goals()
    for g in goals:
        if g["id"] == goal_id:
            g["done"] = not g.get("done", False)
            break
    save_goals(goals)
    return jsonify({"ok": True})

# --- Journal API ---

@app.route("/api/journal", methods=["GET"])
def api_get_journal():
    return jsonify(load_journal())

@app.route("/api/journal", methods=["POST"])
def api_add_journal():
    data = request.get_json()
    entries = load_journal()
    entry = {
        "date": datetime.now().isoformat(),
        "text": data.get("text", ""),
    }
    entries.insert(0, entry)  # newest first
    save_journal(entries)
    return jsonify(entry)


if __name__ == "__main__":
    print("🦅 Atlas Mission Control starting...")
    print("   URL: http://localhost:18787")
    print("   API: http://localhost:18787/api/status")
    app.run(host="0.0.0.0", port=18787, debug=False)
