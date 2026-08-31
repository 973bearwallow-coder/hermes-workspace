import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import harness

class HarnessTests(unittest.TestCase):
    def test_missing_model_blocks(self):
        with tempfile.TemporaryDirectory() as td, patch.object(harness, "gpu_state", return_value={"ok": True, "memory_free_mib": 20000}):
            r = harness.preflight(Path(td)/"missing", Path(td)/"out")
            self.assertFalse(r["ready"])
            self.assertIn("model directory absent", r["reasons"])

    def test_vram_contention_blocks(self):
        with tempfile.TemporaryDirectory() as td, patch.object(harness, "gpu_state", return_value={"ok": True, "memory_free_mib": 1000}):
            model = Path(td)/"model"; model.mkdir()
            r = harness.preflight(model, Path(td)/"out")
            self.assertFalse(r["ready"])
            self.assertTrue(any("VRAM" in x for x in r["reasons"]))

if __name__ == "__main__":
    unittest.main()
