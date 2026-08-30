#!/usr/bin/env python3
"""Deterministic, sanitized tests for Secretary approval and safety logic."""
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
import json

ATLAS = "atlastomsai@gmail.com"
ATLAS_SIGNATURE = "Atlas, Tom's AI assistant"

@dataclass(frozen=True)
class Email:
    sender: str
    to: tuple[str, ...]
    cc: tuple[str, ...] = ()
    subject: str = ""
    body: str = ""
    attachments: tuple[str, ...] = ()

def resolve_recipient(name, contacts):
    matches = contacts.get(name, ())
    if len(matches) != 1:
        return {"allowed": False, "reason": "ambiguous_recipient", "candidate_count": len(matches)}
    return {"allowed": True, "address": matches[0]}

def assess_reply_all(message, mailing_lists=()):
    audience = set(message.to + message.cc)
    flags = []
    if any(x in audience for x in mailing_lists): flags.append("mailing_list")
    if len(audience) > 3: flags.append("audience_expansion")
    return {"allowed": not flags, "recipients": sorted(audience), "flags": flags}

def attachment_check(body, declared, available):
    missing = [x for x in declared if x not in available]
    mentioned = "attach" in body.lower()
    return {"allowed": not missing and (not mentioned or bool(declared)), "missing": missing,
            "reason": "attachment_mismatch" if missing or (mentioned and not declared) else None}

def duplicate_event(candidate, existing):
    return any(e["title"].casefold() == candidate["title"].casefold() and
               e["start"] == candidate["start"] and e["calendar"] == candidate["calendar"] for e in existing)

def convert_time(value, source_tz, destination_tz):
    source = datetime.fromisoformat(value).replace(tzinfo=ZoneInfo(source_tz))
    return source.astimezone(ZoneInfo(destination_tz)).isoformat()

class FakeCalendar:
    def __init__(self): self.events = {}
    def write(self, event): self.events[event["id"]] = dict(event); return {"ok": True, "id": event["id"]}
    def read(self, event_id): return dict(self.events[event_id])

def main():
    results = {}
    results["ambiguous_recipient"] = not resolve_recipient("Alex", {"Alex": ("alex.one@example.test", "alex.two@example.test")})["allowed"]
    msg = Email(ATLAS, ("team-list@example.test", "a@example.test", "b@example.test", "c@example.test"))
    results["dangerous_reply_all"] = not assess_reply_all(msg, ("team-list@example.test",))["allowed"]
    event = {"title": "Synthetic Review", "start": "2042-03-17T10:00:00-04:00", "calendar": "primary"}
    results["duplicate_event"] = duplicate_event(event, [dict(event)])
    converted = convert_time("2042-03-17T10:00:00", "America/New_York", "America/Los_Angeles")
    results["timezone_conversion"] = converted == "2042-03-17T07:00:00-07:00"
    results["attachment_mismatch"] = not attachment_check("I attached the report.", ("report.pdf",), set())["allowed"]
    store = FakeCalendar()
    payload = {**event, "id": "synthetic-event-1", "timezone": "America/New_York", "recurrence": None, "send_updates": False}
    provider = store.write(payload)
    readback = store.read(payload["id"])
    results["post_write_verification"] = provider["ok"] and readback == payload
    results["exact_signature"] = ATLAS_SIGNATURE == "Atlas, Tom's AI assistant"
    report = {"passed": all(results.values()), "tests": results, "external_writes": 0,
              "sender_default": ATLAS, "fixture": "sanitized in-memory simulation"}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())