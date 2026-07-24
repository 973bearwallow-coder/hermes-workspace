#!/usr/bin/env python3
"""Stress-test Atlas Butler endpoints for weak spots.

Runs a small suite against /talk and /talk_stream using override_text so we can
isolate routing / memory / prompt behavior without STT noise.

Outputs a concise human-readable report; exits 0 unless the harness itself fails.
"""

from __future__ import annotations

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any

import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(InsecureRequestWarning)
BASE = "https://127.0.0.1:8765"
TIMEOUT = 120

CASES = [
    "beef enchilada recipe",
    "the recipe",
    "what was the recipe again",
    "make the recipe bigger",
    "Tuesday night invite",
    "Thursday night drinking club invite",
    "the invite",
    "what centerfold did I pick",
    "which one did I pick",
    "set a reminder for tomorrow at 9am to call Jane",
    "atlas text Jane and set a reminder for tomorrow",
    "atlas call Jane tomorrow morning",
    "hey atlas can you help me",
    "uh the thing about the invite",
    "okay so the recipe",
    "what did I say about the recipe earlier",
]

SUSPICIOUS = [
    "clipping your words",
    "didn't catch",
    "can't help",
]

@dataclass
class Result:
    endpoint: str
    query: str
    status: int
    reply: str
    error: str = ""
    elapsed: float = 0.0


def talk(query: str) -> Result:
    t0 = time.time()
    try:
        r = requests.post(
            f"{BASE}/talk",
            json={"override_text": query},
            timeout=TIMEOUT,
            verify=False,
        )
        reply = ""
        try:
            reply = r.json().get("reply", "")
        except Exception:
            reply = r.text[:400]
        return Result("talk", query, r.status_code, reply, elapsed=time.time() - t0)
    except Exception as e:
        return Result("talk", query, 0, "", error=str(e), elapsed=time.time() - t0)


def talk_stream(query: str) -> Result:
    t0 = time.time()
    try:
        r = requests.post(
            f"{BASE}/talk_stream",
            json={"override_text": query},
            timeout=TIMEOUT,
            verify=False,
            stream=True,
        )
        chunks: list[str] = []
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            chunks.append(line)
            if '"type": "done"' in line or "\"done\": true" in line:
                break
        return Result("talk_stream", query, r.status_code, "\n".join(chunks[-3:]), elapsed=time.time() - t0)
    except Exception as e:
        return Result("talk_stream", query, 0, "", error=str(e), elapsed=time.time() - t0)


def suspicious(reply: str) -> list[str]:
    low = (reply or "").lower()
    return [s for s in SUSPICIOUS if s in low]


def main() -> int:
    quiet_clean = "--quiet-clean" in __import__("sys").argv or __import__("os").environ.get("BUTLER_STRESS_QUIET") == "1"
    if not quiet_clean:
        print("== Butler stress test ==")
        print(f"Base: {BASE}")

    # Basic sequential checks.
    results: list[Result] = []
    for q in CASES:
        results.append(talk(q))
        results.append(talk_stream(q))

    # Small concurrency burst.
    burst_queries = [
        "beef enchilada recipe",
        "the recipe",
        "what centerfold did I pick",
    ]
    print("-- concurrency burst --")
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = [ex.submit(talk, q) for q in burst_queries]
        for fut in as_completed(futs):
            results.append(fut.result())

    weaknesses: list[str] = []
    for r in results:
        if r.status != 200:
            weaknesses.append(f"{r.endpoint} {r.query!r}: HTTP {r.status} ({r.error or 'no body'})")
        if r.error:
            weaknesses.append(f"{r.endpoint} {r.query!r}: error {r.error}")
        if r.reply:
            bad = suspicious(r.reply)
            if bad:
                weaknesses.append(f"{r.endpoint} {r.query!r}: suspicious language {bad} -> {r.reply[:180]}")
        if r.elapsed > 20:
            weaknesses.append(f"{r.endpoint} {r.query!r}: slow response {r.elapsed:.1f}s")

    # Extra heuristics: if follow-up doesn't reference prior subject, flag it.
    followup = next((r for r in results if r.endpoint == "talk" and r.query == "the recipe"), None)
    if followup and "beef enchilada" not in followup.reply.lower() and "recipe" not in followup.reply.lower():
        weaknesses.append(f"follow-up handling: 'the recipe' did not anchor back to the prior subject -> {followup.reply[:180]}")

    # Print a concise report.
    if weaknesses:
        print("\n== weaknesses found ==")
        for w in weaknesses:
            print("-", w)
    elif not quiet_clean:
        print("\nNo new weaknesses found in this pass.")

    if not quiet_clean:
        print("\n== sample replies ==")
        for r in results[:10]:
            reply = r.reply.replace("\n", " ")[:220]
            print(f"- [{r.endpoint}] {r.query!r} -> {reply}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
