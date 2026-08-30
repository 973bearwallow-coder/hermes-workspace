import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).with_name("mission_control.py")
spec = importlib.util.spec_from_file_location("mission_control", MODULE_PATH)
mc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mc)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    registry = {
        "contact": {
            "voice_url": "https://atlas.test/voice",
            "telegram_url": "https://web.telegram.org/",
        },
        "apps": [
            {
                "id": "voice",
                "name": "Atlas Voice",
                "description": "Talk naturally with Atlas.",
                "url": "https://atlas.test/voice",
                "health_url": "http://127.0.0.1:9/health",
                "icon": "mic",
                "featured": True,
            }
        ],
    }
    registry_path = tmp_path / "mission_control.json"
    registry_path.write_text(json.dumps(registry))
    monkeypatch.setattr(mc, "REGISTRY_FILE", registry_path)
    monkeypatch.setattr(
        mc,
        "get_tasks",
        lambda: [
            {"id": "1", "title": "Build Mission Control", "detail": "Clean home screen", "status": "running", "priority": 1},
            {"id": "2", "title": "Paw Prints website", "detail": "Waiting for Tom and Jane", "status": "blocked", "priority": 1},
            {"id": "3", "title": "Morning briefing integration", "detail": "Connect the briefing", "status": "ready", "priority": 3},
        ],
    )
    monkeypatch.setattr(mc, "probe_app", lambda app: {**app, "status": "ready", "status_label": "Ready"})
    mc.app.config.update(TESTING=True)
    return mc.app.test_client()


def test_home_is_sparse_and_action_oriented(client):
    response = client.get("/")
    text = response.get_data(as_text=True)
    assert response.status_code == 200
    for expected in [
        "Talk to Atlas",
        "Needs Your Attention",
        "Active Work",
        "Upcoming Projects",
        "Your Apps",
        "Build Mission Control",
        "Paw Prints website",
        "Morning briefing integration",
        "Atlas Voice",
    ]:
        assert expected in text
    for clutter in ["Disk Space", "Recent Cron Jobs", "Memory &amp; Activity", "Pet Community Intel", "token count"]:
        assert clutter not in text


def test_home_is_mobile_ready_and_self_contained(client):
    text = client.get("/").get_data(as_text=True)
    assert 'name="viewport"' in text
    assert "@media (max-width: 720px)" in text
    assert "cdn.tailwindcss.com" not in text
    assert "cdnjs.cloudflare.com" not in text
    assert 'rel="manifest"' in text
    assert 'href="https://atlas.test/voice"' in text


def test_task_sections_are_normalized_without_duplication():
    tasks = [
        {"id": "run", "title": "Running", "detail": "", "status": "running", "priority": 1},
        {"id": "blocked", "title": "Blocked", "detail": "Need Tom", "status": "blocked", "priority": 1},
        {"id": "ready", "title": "Ready", "detail": "", "status": "ready", "priority": 2},
        {"id": "done", "title": "Done", "detail": "", "status": "done", "priority": 1},
    ]
    sections = mc.organize_tasks(tasks)
    assert [x["id"] for x in sections["active"]] == ["run"]
    assert [x["id"] for x in sections["attention"]] == ["blocked"]
    assert [x["id"] for x in sections["upcoming"]] == ["ready"]
    assert not any(x["id"] == "done" for values in sections.values() for x in values)


def test_status_api_uses_human_readable_states(client):
    payload = client.get("/api/status").get_json()
    assert payload["summary"] == "Ready"
    assert payload["apps"][0]["status"] == "ready"
    assert payload["apps"][0]["status_label"] == "Ready"
    assert payload["counts"] == {"attention": 1, "active": 1, "upcoming": 1}
    assert "health_url" not in payload["apps"][0]


def test_manifest_and_service_worker_exist(client):
    manifest = client.get("/manifest.webmanifest")
    assert manifest.status_code == 200
    assert manifest.get_json()["name"] == "Atlas Mission Control"
    worker = client.get("/sw.js")
    assert worker.status_code == 200
    assert "mission-control-v1" in worker.get_data(as_text=True)


def test_get_tasks_reads_native_kanban_schema(tmp_path, monkeypatch):
    import sqlite3

    db_path = tmp_path / "kanban.db"
    db = sqlite3.connect(db_path)
    db.execute(
        "CREATE TABLE tasks (id TEXT, title TEXT, body TEXT, status TEXT, priority INTEGER, created_at INTEGER)"
    )
    db.executemany(
        "INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?)",
        [
            ("queued", "Queued project", "Useful detail", "ready", 2, 10),
            ("finished", "Finished project", "Old detail", "done", 1, 5),
        ],
    )
    db.commit()
    db.close()
    monkeypatch.setattr(mc, "KANBAN_DB", db_path)
    assert mc.get_tasks() == [
        {
            "id": "queued",
            "title": "Queued project",
            "detail": "Useful detail",
            "status": "ready",
            "priority": 2,
            "created_at": 10,
        }
    ]


def test_registry_rejects_unsafe_or_incomplete_entries(tmp_path, monkeypatch):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"apps": [{"id": "oops", "name": "Oops", "url": "javascript:alert(1)"}]}))
    monkeypatch.setattr(mc, "REGISTRY_FILE", bad)
    with pytest.raises(ValueError):
        mc.load_registry()


def test_live_registry_atlas_voice_uses_real_hands_free_bridge():
    registry = json.loads(Path("/home/tom/hermes-workspace/data/mission_control.json").read_text())
    atlas_voice = next(app for app in registry["apps"] if app["name"] == "Atlas Voice")
    expected = "https://charles-1.taila0a481.ts.net:8443/"
    assert registry["contact"]["voice_url"] == expected
    assert atlas_voice["url"] == expected
