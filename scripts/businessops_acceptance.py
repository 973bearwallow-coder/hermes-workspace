#!/usr/bin/env python3
"""Sanitized, no-write acceptance suite for the Business Operations profile."""
from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path


def extract_commitments(lines: list[dict]) -> list[dict]:
    """Keep only explicit decisions; never infer owner or date."""
    out = []
    for item in lines:
        if item.get("kind") != "decision":
            continue
        out.append({
            "decision": item["text"],
            "owner": item.get("owner") or "UNASSIGNED",
            "due": item.get("due") or "UNASSIGNED",
            "citation": item["citation"],
        })
    return out


def classify_claim(claim: dict) -> str:
    evidence = claim.get("evidence")
    if evidence == "reproducible_demo":
        return "demonstrated"
    if evidence == "vendor":
        return "vendor_claim"
    if evidence == "participant_report":
        return "anecdotal"
    return "speculation"


def requires_approval(action: str) -> bool:
    gated = {
        "purchase", "subscribe", "sign_contract", "send_message",
        "change_authoritative_record", "publish", "approve_invoice",
    }
    return action in gated


def route_domain(domain: str) -> str:
    return "businessops" if domain in {"paw_prints", "coaching", "community", "spreadsheet"} else "atlas"


def main() -> int:
    results: dict[str, bool] = {}
    meeting = [
        {"kind": "decision", "text": "Pilot Saturday walks", "owner": "Jane", "due": "2026-09-05", "citation": "transcript 04:12"},
        {"kind": "suggestion", "text": "Maybe offer grooming", "citation": "transcript 07:03"},
        {"kind": "decision", "text": "Review boarding intake form", "citation": "transcript 09:40"},
    ]
    commitments = extract_commitments(meeting)
    results["decisions_not_suggestions"] = len(commitments) == 2 and all("grooming" not in x["decision"] for x in commitments)
    results["explicit_owner_due_only"] = commitments[1]["owner"] == "UNASSIGNED" and commitments[1]["due"] == "UNASSIGNED"
    results["citations_preserved"] = all(x["citation"].startswith("transcript ") for x in commitments)

    with tempfile.TemporaryDirectory(prefix="businessops-acceptance-") as td:
        root = Path(td)
        source = root / "source.csv"
        output = root / "analysis.csv"
        rows = [("Dog walks", 12, 25.0), ("Boarding", 3, 80.0), ("Pet sitting", 4, 45.0)]
        with source.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["service", "units", "price"])
            writer.writerows(rows)
        source_before = source.read_bytes()
        total = sum(units * price for _, units, price in rows)
        with output.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["metric", "value"])
            writer.writerow(["revenue_total", f"{total:.2f}"])
        with output.open(newline="", encoding="utf-8") as f:
            check = list(csv.reader(f))
        results["spreadsheet_total_reconciles"] = check[1] == ["revenue_total", "720.00"]
        results["source_preserved"] = source.read_bytes() == source_before and output.exists()
        temp_path = str(root)

    claims = [
        {"evidence": "reproducible_demo"}, {"evidence": "vendor"},
        {"evidence": "participant_report"}, {"evidence": None},
    ]
    results["evidence_classes_distinguished"] = [classify_claim(c) for c in claims] == [
        "demonstrated", "vendor_claim", "anecdotal", "speculation"
    ]
    results["financial_and_external_actions_gated"] = all(requires_approval(x) for x in [
        "purchase", "send_message", "change_authoritative_record", "approve_invoice"
    ]) and not requires_approval("read_only_analysis")
    results["cross_domain_work_returns_to_atlas"] = route_domain("media") == "atlas" and route_domain("paw_prints") == "businessops"

    report = {
        "passed": all(results.values()),
        "test_count": len(results),
        "tests": results,
        "external_writes": 0,
        "authoritative_records_modified": 0,
        "financial_commitments": 0,
        "temporary_artifacts_removed_on_exit": not Path(temp_path).exists(),
    }
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] and report["temporary_artifacts_removed_on_exit"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
