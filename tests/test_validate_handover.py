import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_handover.py"
spec = importlib.util.spec_from_file_location("validate_handover", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT}")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

VALID = """# Autonomous Project Handover
**Date**: 2026-09-01
**Session ID**: abc
**Agent**: Atlas
**Task**: Verify handovers
**Status**: ready_for_review
## Objective and Acceptance Criteria
- [x] Validator exits zero
## Current State
- Good
## Completed Work
- Added validator
## Remaining Work
- None
## Blockers / Risks
- None
## Changed Files
| Path | Purpose | Verified? |
|---|---|---|
| `/tmp/a` | test | yes |
## Commands and Test Results
| Command/check | Actual result |
|---|---|
| `python test.py` | 2 passed |
## Git / Rollback Checkpoint
- Clean
## Decisions and Guardrails
- No secrets
## Exact Next Action
1. Deliver
"""


class HandoverValidatorTests(unittest.TestCase):
    def test_valid_handover(self):
        self.assertEqual([], mod.validate(VALID))

    def test_template_is_not_valid_delivery(self):
        errors = mod.validate("**Status**: complete\n## Completed Work\n- done")
        self.assertTrue(any("missing section" in e for e in errors))
        self.assertTrue(any("acceptance criterion" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
