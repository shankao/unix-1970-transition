# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from punch_era import checked_name, checked_records, replay_text


class PublicPunchTests(unittest.TestCase):
    def test_native_name_and_entry_validation(self):
        self.assertEqual("try.o", checked_name("try.o"))
        for bad in ("A.o", "too-long.o", "x;rm.o", "plain"):
            with self.assertRaises(ValueError):
                checked_name(bad)
        records = checked_records("i 001000 000000\n", 0o1000)
        self.assertEqual(1, len(records))
        with self.assertRaises(ValueError):
            checked_records("i 001000 000000\n", 0o1002)

    def test_replay_deposits_only_front_panel_bootstrap(self):
        text = replay_text("try", 0o1000)
        deposits = [line for line in text.splitlines() if line.startswith("deposit ")]
        self.assertEqual(14, len(deposits))
        self.assertTrue(all(0o57744 <= int(line.split()[1], 8) <= 0o57776
                            for line in deposits))
        self.assertIn("attach ptr artifacts/visitor/try.ptap", text)
        self.assertIn("go 057500", text)


if __name__ == "__main__":
    unittest.main()
