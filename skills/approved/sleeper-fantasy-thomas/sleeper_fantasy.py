#!/usr/bin/env python3
"""Read-only Sleeper league snapshot and recommendation-report foundation."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.sleeper.app/v1"
DEFAULT_USER = "Frost1234"
DEFAULT_LEAGUE = "1312075390298124288"
ID_RE = re.compile(r"^[0-9]{10,24}$")
USER_RE = re.compile(r"^[A-Za-z0-9_.-]{1,50}$")

class SleeperError(RuntimeError): pass

def api_get(path: str):
    req = urllib.request.Request(API + path, headers={"User-Agent": "Amy-Sleeper-ReadOnly/1.0", "Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            if response.status != 200: raise SleeperError(f"Sleeper HTTP {response.status}")
            return json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SleeperError(f"Sleeper read failed: {exc}") from exc

def validate(username: str, league_id: str):
    if not USER_RE.fullmatch(username): raise SleeperError("Invalid Sleeper username format")
    if not ID_RE.fullmatch(league_id): raise SleeperError("Invalid Sleeper league ID format")

def atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text); handle.flush(); os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try: os.unlink(temporary)
        except FileNotFoundError: pass

def collect(username: str, league_id: str, week: int | None = None):
    validate(username, league_id)
    user = api_get(f"/user/{username}")
    if not user: raise SleeperError("Sleeper user not found")
    league = api_get(f"/league/{league_id}")
    if not league: raise SleeperError("Sleeper league not found")
    if league.get("sport") != "nfl": raise SleeperError("League is not an NFL league")
    rosters = api_get(f"/league/{league_id}/rosters")
    users = api_get(f"/league/{league_id}/users")
    user_id = str(user.get("user_id", ""))
    roster = next((r for r in rosters if str(r.get("owner_id", "")) == user_id), None)
    result = {"observed_at": dt.datetime.now(dt.timezone.utc).isoformat(), "source": API,
              "user": {"username": user.get("username"), "display_name": user.get("display_name"), "user_id": user_id},
              "league": league, "roster": roster, "league_users": users}
    if week is not None and 1 <= week <= 18:
        result["week"] = week
        result["matchups"] = api_get(f"/league/{league_id}/matchups/{week}")
        result["transactions"] = api_get(f"/league/{league_id}/transactions/{week}")
    return result

def render(snapshot, report_type: str):
    league, user, roster = snapshot["league"], snapshot["user"], snapshot.get("roster")
    lines = [f"# {report_type.title()} report", "", f"Observed: {snapshot['observed_at']}",
             f"Source: {snapshot['source']}", f"League: {league.get('name')} ({league.get('league_id')})",
             f"Season/status: {league.get('season')} / {league.get('status')}", f"Manager: {user.get('display_name')}", ""]
    if not roster:
        lines += ["Thomas does not yet have an owned roster in the current Sleeper response.",
                  "No player recommendation is made until the draft or roster assignment is visible."]
    else:
        starters = roster.get("starters") or []
        players = roster.get("players") or []
        reserve = roster.get("reserve") or []
        lines += [f"Roster ID: {roster.get('roster_id')}", f"Players: {len(players)}; starters: {len(starters)}; reserve: {len(reserve)}", "",
                  "This report is read-only. Verify current injury news, official inactive lists, projections, and available-player data before deciding.",
                  "Amy may recommend a primary option and backup, but Thomas must execute every lineup, waiver, trade, or roster move himself."]
    return "\n".join(lines) + "\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default=DEFAULT_USER)
    parser.add_argument("--league-id", default=DEFAULT_LEAGUE)
    parser.add_argument("--week", type=int)
    parser.add_argument("--report", choices=("waiver", "lineup", "inactives", "snapshot"), default="snapshot")
    parser.add_argument("--output-dir", default=str(Path.home()/".hermes"/"fantasy-football"/"reports"))
    args = parser.parse_args()
    snapshot = collect(args.username, args.league_id, args.week)
    out = Path(args.output_dir)
    atomic_write(out/"latest_snapshot.json", json.dumps(snapshot, indent=2, sort_keys=True)+"\n")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = out/f"{stamp}-{args.report}.md"
    atomic_write(report_path, render(snapshot, args.report))
    print(json.dumps({"ok": True, "report": str(report_path), "league": snapshot["league"].get("name"), "status": snapshot["league"].get("status"), "roster_found": bool(snapshot.get("roster")), "read_only": True}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
