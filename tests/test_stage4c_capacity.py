from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_stage4c_capacity import CASES, capacity_source
import pdp11_oracle as oracle


class Stage4CCapacityTests(unittest.TestCase):
    def test_matrix_includes_requested_points(self):
        for point in ((17, 5), (24, 5), (32, 5), (40, 5), (48, 10)):
            self.assertIn(point, CASES)

    def test_generated_capacity_counts(self):
        for globals_, locals_ in CASES:
            source, expected = capacity_source(globals_, locals_)
            self.assertEqual(globals_, expected.count("a ") + expected.count("l "))
            self.assertEqual(locals_, expected.count("n "))
            self.assertGreater(len(source), 128)

    def test_stage3_shape_has_exact_demand(self):
        text = (ROOT / "tests/pdp7-as11/stage4c-stage3-shaped.s").read_text()
        import re
        globals_ = re.findall(r"(?m)^([a-z_][a-z0-9_]*):", text)
        locals_ = re.findall(r"(?m)(?<![a-z0-9_])([0-9]):", text)
        self.assertEqual(17, len(globals_))
        self.assertEqual(5, len(locals_))
        for mnemonic in ("add", "asl", "asr", "bne", "bpl", "br", "clr",
                         "cmp", "halt", "jmp", "mov", "movb", "tst", "tstb"):
            self.assertIn(mnemonic, text)

    def test_recorded_stage3_shape_decodes_with_oracle(self):
        path = ROOT / "evidence/stage4c-capacity/stage3-shaped.out"
        if not path.exists():
            self.skipTest("native capacity evidence not recorded")
        records = []
        current = None
        for line in path.read_text().splitlines():
            parts = line.split()
            if parts[0] == "i":
                if current:
                    records.append(current)
                current = [int(parts[1], 8), [int(parts[2], 8)]]
            elif parts[0] == "x":
                self.assertIsNotNone(current)
                self.assertEqual(current[0] + 2 * len(current[1]), int(parts[1], 8))
                current[1].append(int(parts[2], 8))
            elif current:
                records.append(current)
                current = None
        if current:
            records.append(current)
        for address, words in records:
            decoded = oracle.decode_one(words, address)
            self.assertEqual(len(words), len(decoded.words))
        self.assertGreaterEqual(len(records), 30)

    def test_recorded_boundary_is_stable(self):
        root = ROOT / "evidence/stage4c-capacity"
        if not root.exists():
            self.skipTest("native capacity evidence not recorded")
        for globals_, locals_ in ((38, 10), (39, 0)):
            observed = (root / f"g{globals_:02d}-l{locals_:02d}.out").read_text()
            self.assertEqual(capacity_source(globals_, locals_)[1], observed)
        for locals_ in (1, 2, 4, 5, 10):
            observed = (root / f"g39-l{locals_:02d}.out").read_text()
            self.assertEqual("e 000051 ph\n", observed[-12:])


if __name__ == "__main__":
    unittest.main()
