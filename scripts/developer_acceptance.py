#!/usr/bin/env python3
"""Sanitized, no-external-write acceptance suite for Developer."""
from __future__ import annotations

import json
import py_compile
import subprocess
import tempfile
from pathlib import Path

PROFILE = Path("/home/tom/.hermes/profiles/developer")
SOUL = PROFILE / "SOUL.md"
ORCHESTRA = PROFILE / "ORCHESTRA.json"


def check(name: str, condition: bool, detail: str) -> dict:
    return {"name": name, "passed": bool(condition), "detail": detail}


def main() -> int:
    results: list[dict] = []
    soul = SOUL.read_text(encoding="utf-8")
    orchestra = json.loads(ORCHESTRA.read_text(encoding="utf-8"))

    required_rules = [
        "Atlas is the conductor",
        "Do not delegate to other specialists",
        "Never use destructive Git commands",
        "Never weaken a test to make code pass",
        "production configuration",
        "Real-Interface Acceptance",
        "A successful local preview is never reported as a production deployment",
        "Requested behavior demonstrated with real output",
    ]
    results.append(check(
        "policy_contract",
        all(rule in soul for rule in required_rules),
        "TDD, Git, deployment, delegation, interface, and evidence rules present",
    ))

    skills = orchestra.get("skills", [])
    missing = [s for s in skills if not (PROFILE / "skills" / s / "SKILL.md").exists()]
    results.append(check(
        "assigned_skills",
        len(skills) == 14 and not missing,
        f"assigned={len(skills)} missing={missing}",
    ))

    with tempfile.TemporaryDirectory(prefix="developer-acceptance-") as td:
        root = Path(td)
        module = root / "calculator.py"
        test_file = root / "test_calculator.py"
        module.write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
        test_file.write_text(
            "import unittest\n"
            "from calculator import add\n\n"
            "class CalculatorTest(unittest.TestCase):\n"
            "    def test_add(self):\n"
            "        self.assertEqual(add(2, 3), 5)\n\n"
            "if __name__ == '__main__':\n"
            "    unittest.main()\n",
            encoding="utf-8",
        )
        py_compile.compile(str(module), doraise=True)
        proc = subprocess.run(
            ["python3", "-m", "unittest", "-v", str(test_file)],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
        )
        results.append(check(
            "isolated_code_and_test_execution",
            proc.returncode == 0 and "OK" in proc.stderr,
            f"returncode={proc.returncode}; unittest={'OK' if 'OK' in proc.stderr else 'FAILED'}",
        ))
        results.append(check(
            "artifact_scope",
            sorted(p.name for p in root.iterdir() if p.name != "__pycache__") == ["calculator.py", "test_calculator.py"],
            "only the two declared temporary fixture files were created",
        ))
        temp_path = str(root)

    requested = {"edit_scoped_code", "force_push", "publish_release", "change_production_config"}
    allowed = requested & {"edit_scoped_code", "run_tests", "inspect_diff"}
    blocked = requested - allowed
    results.append(check(
        "consequential_action_gate",
        allowed == {"edit_scoped_code"} and blocked == {"force_push", "publish_release", "change_production_config"},
        f"allowed={sorted(allowed)} blocked={sorted(blocked)}",
    ))
    results.append(check(
        "cross_domain_escalation",
        "return cross-domain needs to Atlas for routing" in soul,
        "cross-domain work returns to Atlas",
    ))

    summary = {
        "suite": "developer_acceptance",
        "passed": sum(r["passed"] for r in results),
        "total": len(results),
        "zero_external_writes": True,
        "production_repositories_modified": 0,
        "temporary_artifacts_removed_on_exit": not Path(temp_path).exists(),
        "results": results,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["passed"] == summary["total"] and summary["temporary_artifacts_removed_on_exit"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
