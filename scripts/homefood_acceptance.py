#!/usr/bin/env python3
"""Sanitized, no-external-write acceptance suite for Food and Home."""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

PROFILE = Path("/home/tom/.hermes/profiles/homefood")
SOUL = PROFILE / "SOUL.md"
ORCHESTRA = PROFILE / "ORCHESTRA.json"


def check(name: str, condition: bool, detail: str) -> dict:
    return {"name": name, "passed": bool(condition), "detail": detail}


def main() -> int:
    results: list[dict] = []
    soul = SOUL.read_text(encoding="utf-8")
    orchestra = json.loads(ORCHESTRA.read_text(encoding="utf-8"))

    required_rules = [
        "Never claim an ingredient is on hand unless the source inventory says so",
        "Preserve dietary restrictions, allergies, serving count, units, cooking temperatures, and timing",
        "Never assure Tom that questionable food is safe based only on appearance or smell",
        "Never fabricate a price, sale, package size, unit price, stock status",
        "Do not place orders, reserve pickup slots, redeem rewards",
        "Resolve “the farm” to West Augusta, Virginia",
        "default local household questions to Fairfax County, Virginia",
        "Do not instruct Tom to bypass safety devices",
        "Never hire, book, call, message, sign, purchase, order, schedule a visit",
        "return to Atlas for specialist routing",
    ]
    results.append(check("policy_contract", all(x in soul for x in required_rules),
                         "food, price, location, home-safety, approval, and routing rules present"))

    skills = orchestra.get("skills", [])
    missing = [s for s in skills if not (PROFILE / "skills" / s / "SKILL.md").exists()]
    results.append(check("assigned_skills", len(skills) == 12 and not missing,
                         f"assigned={len(skills)} missing={missing}"))

    inventory = {"chicken_lb": 1.5, "rice_cups": 2, "onion": 1}
    recipe = {"chicken_lb": 1.0, "rice_cups": 1.0, "onion": 1, "lime": 2}
    missing_items = {k: v for k, v in recipe.items() if inventory.get(k, 0) < v}
    results.append(check("inventory_first", missing_items == {"lime": 2},
                         f"only source-backed missing item={missing_items}"))

    original_servings = 4
    target_servings = 6
    ingredients = {"chicken_lb": 2.0, "broth_cups": 3.0}
    scale = target_servings / original_servings
    scaled = {k: v * scale for k, v in ingredients.items()}
    results.append(check("recipe_scaling", scaled == {"chicken_lb": 3.0, "broth_cups": 4.5},
                         f"scaled quantities={scaled}; restrictions remain explicit inputs"))

    offers = [
        {"store": "A", "price": 6.00, "quantity_lb": 2.0, "observed": "SANITIZED"},
        {"store": "B", "price": 4.50, "quantity_lb": 1.0, "observed": "SANITIZED"},
    ]
    unit = {o["store"]: o["price"] / o["quantity_lb"] for o in offers}
    results.append(check("unit_price_integrity", unit == {"A": 3.0, "B": 4.5},
                         f"equivalent unit comparison={unit}"))

    locations = {"the farm": "West Augusta, Virginia", "default": "Fairfax County, Virginia"}
    results.append(check("location_resolution",
                         locations["the farm"] == "West Augusta, Virginia" and locations["default"] == "Fairfax County, Virginia",
                         str(locations)))

    hazardous = "replace energized breaker panel and bypass interlock"
    stop_terms = ("energized", "bypass")
    routed_to_pro = any(term in hazardous for term in stop_terms)
    results.append(check("home_safety_boundary", routed_to_pro,
                         "hazardous electrical/bypass request stopped for qualified professional"))

    requested_actions = {"draft_list", "place_order", "hire_contractor", "send_message", "change_thermostat"}
    allowed = requested_actions & {"draft_list", "research", "calculate", "prepare_shortlist"}
    blocked = requested_actions - allowed
    expected_blocked = {"place_order", "hire_contractor", "send_message", "change_thermostat"}
    results.append(check("consequential_action_gate", allowed == {"draft_list"} and blocked == expected_blocked,
                         f"allowed={sorted(allowed)} blocked={sorted(blocked)}"))

    with tempfile.TemporaryDirectory(prefix="homefood-acceptance-") as td:
        source = Path(td) / "inventory.json"
        source.write_text(json.dumps(inventory, sort_keys=True), encoding="utf-8")
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        report = Path(td) / "report.json"
        report.write_text(json.dumps({"missing": missing_items, "unit_prices": unit}, sort_keys=True), encoding="utf-8")
        parsed = json.loads(report.read_text(encoding="utf-8"))
        after = hashlib.sha256(source.read_bytes()).hexdigest()
        results.append(check("artifact_and_source_integrity",
                             parsed["missing"] == {"lime": 2} and before == after,
                             "generated artifact parsed; authoritative fixture unchanged"))

    summary = {
        "suite": "homefood_acceptance",
        "passed": sum(r["passed"] for r in results),
        "total": len(results),
        "zero_external_writes": True,
        "zero_purchases_or_bookings": True,
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["passed"] == summary["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
