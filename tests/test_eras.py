from pathlib import Path
import hashlib
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from dec_abs import loader_bytes


class EraTests(unittest.TestCase):
    def test_stage_checkpoints_are_snapshots_not_eras(self):
        expected = {"stage-0", "stage-1", "stage-4a", "stage-4b", "stage-4c"}
        self.assertEqual(expected, {path.name for path in (ROOT / "snapshots").glob("stage-*")})
        self.assertFalse(any((ROOT / "eras").glob("stage-*")))
        for name in expected:
            self.assertTrue((ROOT / "snapshots" / name / "pdp7.fs").is_file())

    def test_every_historical_era_has_manifest_and_replay(self):
        expected = {"pdp7-unix", "pdp7-crossdev", "pdp11-crossdev"}
        self.assertEqual(expected, {path.name for path in (ROOT / "eras").iterdir()
                                    if path.is_dir()})
        for name in expected:
            self.assertTrue((ROOT / "eras" / name / "ERA.md").is_file())

    def test_dec_loader_materialization_is_lossless(self):
        source = ROOT / "evidence/b4/DEC-11-L2PC-PO.json"
        data = loader_bytes(source)
        self.assertEqual(182, len(data))
        self.assertEqual("e3a0d273e9fdd764a607a99a4f4c2a510e4c6c926309e6ccfd9b6a93ca989845",
                         hashlib.sha256(data).hexdigest())

    def test_pdp11_human_replays_use_ptr_not_payload_deposits(self):
        era = ROOT / "eras/pdp11-crossdev"
        for name, tape in (("interrupt-trap.simh", "u1-interrupt.ptap"),
                           ("ram-substrate.simh", "u1-ram.ptap")):
            text = (era / name).read_text(encoding="ascii")
            self.assertIn(f"attach ptr ../../artifacts/{tape}", text)
            self.assertIn("go 057744", text)
            self.assertIn("go 057500", text)
            deposits = [line for line in text.splitlines() if line.startswith("deposit ")]
            self.assertEqual(14, len(deposits))
            self.assertTrue(all(0o57744 <= int(line.split()[1], 8) <= 0o57776
                                for line in deposits))


if __name__ == "__main__":
    unittest.main()
