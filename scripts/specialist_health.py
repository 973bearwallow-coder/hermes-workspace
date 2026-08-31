#!/usr/bin/env python3
"""Read-only aggregate health check for Atlas's eight specialist profiles."""
import json
import subprocess
import sys
from pathlib import Path

HERMES = "/home/tom/.hermes/hermes-agent/venv/bin/hermes"
ROOT = Path("/home/tom/hermes-workspace/scripts")
SPECIALISTS = {
    "Charles Systems": ("charlesops", "charlesops_health.py"),
    "Research Scout": ("researchscout", "researchscout_web_stack_test.py"),
    "Developer": ("developer", "developer_acceptance.py"),
    "Memory Librarian": ("memorylibrarian", "memorylibrarian_benchmark.py"),
    "Communications Secretary": ("secretary", "secretary_workflow_test.py"),
    "Media Studio": ("mediastudio", "mediastudio_acceptance.py"),
    "Business Operations": ("businessops", "businessops_acceptance.py"),
    "Food and Home": ("homefood", "homefood_acceptance.py"),
}

def run(command, timeout=240):
    proc = subprocess.run(command, text=True, capture_output=True, timeout=timeout)
    return proc.returncode, (proc.stdout + proc.stderr).strip()

def main():
    results = {}
    for name, (profile, validator) in SPECIALISTS.items():
        profile_rc, profile_text = run([HERMES, "profile", "show", profile])
        profile_ok = profile_rc == 0 and "SOUL.md: exists" in profile_text and "Skills:" in profile_text
        validator_ok = True
        validator_rc = None
        if validator:
            path = ROOT / validator
            if not path.exists():
                validator_ok, validator_rc = False, 127
            else:
                validator_rc, _ = run([sys.executable, str(path)])
                validator_ok = validator_rc == 0
        status = "READY" if profile_ok and validator_ok else "BLOCKED"
        results[name] = {"status": status, "profile": profile, "profile_ok": profile_ok,
                         "validator": validator, "validator_exit": validator_rc}
    overall = "READY" if all(item["status"] == "READY" for item in results.values()) else "BLOCKED"
    print(json.dumps({"overall": overall, "specialists": results}, indent=2, sort_keys=True))
    return 0 if overall == "READY" else 1

if __name__ == "__main__":
    raise SystemExit(main())
