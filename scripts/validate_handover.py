#!/usr/bin/env python3
"""Validate that an autonomous-project handover contains actionable evidence."""
import argparse
import re
from pathlib import Path

REQUIRED_SECTIONS = (
    "Objective and Acceptance Criteria", "Current State", "Completed Work",
    "Remaining Work", "Blockers / Risks", "Changed Files",
    "Commands and Test Results", "Git / Rollback Checkpoint",
    "Decisions and Guardrails", "Exact Next Action",
)
PLACEHOLDERS = ("SESSION_ID", "AGENT_NAME", "TASK_DESCRIPTION", "YYYY-MM-DD")
VALID_STATUS = {"in_progress", "blocked", "ready_for_review", "complete"}


def validate(text: str):
    errors = []
    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^## {re.escape(section)}\s*$", text, re.M):
            errors.append(f"missing section: {section}")
    status = re.search(r"^\*\*Status\*\*:\s*([^\n]+)", text, re.M)
    if not status or status.group(1).strip() not in VALID_STATUS:
        errors.append("status must be one of: " + ", ".join(sorted(VALID_STATUS)))
    if not re.search(r"^- \[[ xX]\] .+", text, re.M):
        errors.append("at least one observable acceptance criterion is required")
    if not re.search(r"\| `?[^|\n]+`? \| [^|\n]+ \|", text):
        errors.append("commands/test-results table must include an evidence row")
    for placeholder in PLACEHOLDERS:
        if placeholder in text:
            errors.append(f"unresolved placeholder: {placeholder}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handover", type=Path)
    args = parser.parse_args(argv)
    errors = validate(args.handover.read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"VALID: {args.handover}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
