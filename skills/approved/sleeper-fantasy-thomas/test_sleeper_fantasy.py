#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

path = Path(__file__).with_name("sleeper_fantasy.py")
spec = importlib.util.spec_from_file_location("sleeper_fantasy", path)
mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod; spec.loader.exec_module(mod)

class FakeResponse:
    status = 200
    def __init__(self, payload): self.payload = payload
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return json.dumps(self.payload).encode()

def fake_urlopen(request, timeout=0):
    url = request.full_url
    assert request.method == "GET"
    if url.endswith("/user/Frost1234"): return FakeResponse({"username":"frost1234","display_name":"Frost1234","user_id":"u1"})
    if url.endswith("/league/1312075390298124288"): return FakeResponse({"league_id":"1312075390298124288","name":"Fantasy Football League","sport":"nfl","season":"2026","status":"pre_draft"})
    if url.endswith("/rosters"): return FakeResponse([{"owner_id":"u1","roster_id":1,"players":[],"starters":[]}])
    if url.endswith("/users"): return FakeResponse([{"user_id":"u1","display_name":"Frost1234"}])
    raise AssertionError(url)

mod.urllib.request.urlopen = fake_urlopen
snapshot = mod.collect("Frost1234", "1312075390298124288")
assert snapshot["league"]["sport"] == "nfl"
assert snapshot["roster"]["roster_id"] == 1
assert "read-only" in mod.render(snapshot, "waiver").lower()
try:
    mod.validate("bad user!", "x")
    raise AssertionError("invalid identifiers accepted")
except mod.SleeperError: pass
print(json.dumps({"passed": True, "tests": 4, "external_writes": 0, "sleeper_mutations": 0}))
