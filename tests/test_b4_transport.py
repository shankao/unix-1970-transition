# SPDX-License-Identifier: GPL-3.0-only
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dec_abs import parse_absolute, words_from_bytes
from run_stage3_gold import parse_trace


class B4TransportEvidenceTests(unittest.TestCase):
    def test_pdp7_punched_artifacts_equal_native_u1_maps(self):
        names = (("u1int", "u1-interrupt"), ("u1ram", "u1-ram"))
        for stem, artifact in names:
            trace = parse_trace(
                (ROOT / f"evidence/b4/{stem}-native-trace.txt").read_text())
            memory, transfer, _ = parse_absolute(
                (ROOT / f"artifacts/{artifact}.ptap").read_bytes())
            self.assertEqual(words_from_bytes(memory),
                             {item.address: item.word for item in trace})
            self.assertEqual(transfer, 1)

    def test_historical_runner_deposits_only_front_panel_bootstrap(self):
        source = (ROOT / "tools/run_b4_transport.py").read_text()
        self.assertIn("for offset, word in enumerate(BOOTSTRAP)", source)
        self.assertNotIn("deposit {item.address", source)
        self.assertNotIn("dep {item.address", source)


if __name__ == "__main__":
    unittest.main()
