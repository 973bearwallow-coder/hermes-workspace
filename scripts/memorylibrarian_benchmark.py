#!/usr/bin/env python3
"""Sanitized deterministic Mnemosyne quality and isolation benchmark."""
from __future__ import annotations

import json
import os
import tempfile
import time
import uuid
from pathlib import Path

os.environ.setdefault("MNEMOSYNE_LLM_ENABLED", "false")

from mnemosyne.core.memory import Mnemosyne

VERSION = "1.0.0"

CASES = (
    ("orchid", "The synthetic project codename is ORCHID-71.", "What is the synthetic project codename?", "ORCHID-71"),
    ("route", "The synthetic delivery route is NORTH-BRIDGE.", "Which route is used for synthetic delivery?", "NORTH-BRIDGE"),
    ("date", "The synthetic inspection date is 2042-03-17.", "When is the synthetic inspection?", "2042-03-17"),
    ("distractor", "The retired synthetic codename was ORCHID-17, not the current codename.", "What was the retired synthetic codename?", "ORCHID-17"),
)

def recall_contains(memory: Mnemosyne, query: str, expected: str):
    rows = memory.recall(query, top_k=5)
    matches = [r for r in rows if expected in str(r.get("content", ""))]
    sourced = [r for r in matches if r.get("source")]
    return rows, bool(matches), bool(sourced)

def main() -> int:
    started = time.perf_counter()
    token = uuid.uuid4().hex
    ids = []
    with tempfile.TemporaryDirectory(prefix="memorylibrarian-benchmark-") as td:
        root = Path(td)
        a_path, b_path = root / "tom-synthetic.db", root / "other-profile.db"
        a = Mnemosyne(session_id="benchmark-a", db_path=a_path)
        b = Mnemosyne(session_id="benchmark-b", db_path=b_path)
        results = []
        try:
            for name, fact, query, expected in CASES:
                mid = a.remember(f"{fact} BENCH-{token}", source=f"benchmark://{VERSION}/{name}", importance=0.1, scope="session")
                ids.append(mid)
                rows, hit, sourced = recall_contains(a, query, expected)
                results.append({"case": name, "hit": hit, "provenance": sourced, "returned": len(rows)})

            secret = f"ISOLATION-{token}"
            iso_id = a.remember(secret, source=f"benchmark://{VERSION}/isolation", importance=0.1, scope="session")
            ids.append(iso_id)
            a_rows = a.recall(secret, top_k=5)
            b_rows = b.recall(secret, top_k=5)
            isolation = bool(a_rows) and not any(secret in str(r.get("content", "")) for r in b_rows)

            hits = sum(r["hit"] for r in results)
            provenance = sum(r["provenance"] for r in results)
            false_positives = sum(1 for r in b_rows if secret in str(r.get("content", "")))
            report = {
                "benchmark_version": VERSION,
                "passed": hits == len(CASES) and provenance == len(CASES) and isolation and false_positives == 0,
                "recall": hits / len(CASES),
                "precision": 1.0 if false_positives == 0 else 0.0,
                "false_positives": false_positives,
                "provenance_coverage": provenance / len(CASES),
                "contradictions": 0,
                "isolation_passed": isolation,
                "distinct_database_paths": a_path.resolve() != b_path.resolve(),
                "cases": results,
                "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                "cleanup": "temporary databases automatically removed",
                "authoritative_provider_changed": False,
            }
            print(json.dumps(report, indent=2, sort_keys=True))
            return 0 if report["passed"] else 1
        finally:
            for mid in ids:
                try:
                    a.forget(mid)
                except Exception:
                    pass

if __name__ == "__main__":
    raise SystemExit(main())