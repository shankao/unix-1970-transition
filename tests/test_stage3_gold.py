from pathlib import Path
import hashlib
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_stage3_gold import parse_trace, simh_script, validate_stage3b_l


class Stage3GoldTests(unittest.TestCase):
    def test_only_development_pdp7_is_unthrottled(self):
        active = (ROOT / "machines/pdp7/pdp7-unix/build/unixv0.simh").read_text()
        self.assertIn("set nothrottle", active)
        self.assertNotIn("set throttle 400K", active)
        expected = "c6c9f0368073c43056e3b4ed0359889ef080c908c842e9f8d7e709748a51dbe6"
        for config in sorted((ROOT / "eras").glob("stage-*/pdp7.simh")):
            with self.subTest(config=config):
                self.assertEqual(expected, hashlib.sha256(config.read_bytes()).hexdigest())
                self.assertIn("set throttle 400K", config.read_text())

    def test_terminal_transfer_pacing_is_unchanged(self):
        runner = (ROOT / "tools/run_stage4a.py").read_text(encoding="utf-8")
        self.assertIn("time.sleep(0.08)", runner)

    def test_malformed_duplicate_and_conflicting_records_fail(self):
        for text in (
            "i 001000 012700\njunk\n",
            "i 001000 012700\nw 001000 000001\n",
            "i 001001 012700\n",
            "",
        ):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_trace(text)

    def test_deposits_are_literal_native_records(self):
        records = parse_trace("l start 001000\ni 001000 000000\nw 001002 177777\n")
        script = simh_script(records, Path("transcript.txt"))
        self.assertIn("dep 001000 000000", script)
        self.assertIn("dep 001002 177777", script)
        self.assertNotIn("encode(", script)

    def test_runner_has_no_encoder_and_invokes_native_as11(self):
        runner = (ROOT / "tools/run_stage3_gold.py").read_text(encoding="utf-8")
        self.assertNotIn("from pdp11_oracle import encode", runner)
        self.assertNotIn("def encode", runner)
        self.assertIn('session.command("a.out gold.s gold.o"', runner)
        self.assertIn('trace = clean_cat(session.command("cat gold.o"', runner)

    def test_recorded_native_trace_is_complete_and_oracle_validated(self):
        path = ROOT / "evidence/stage3-gold/native-trace.txt"
        if not path.exists():
            self.skipTest("native gold evidence not recorded")
        records = parse_trace(path.read_text(encoding="ascii"))
        validate_stage3b_l(records)
        script = (ROOT / "evidence/stage3-gold/test-l.simh").read_text()
        deposits = {
            tuple(int(part, 8) for part in line.split()[1:])
            for line in script.splitlines() if line.startswith("dep ")
        }
        self.assertEqual({(item.address, item.word) for item in records}, deposits)

    def test_recorded_execution_reaches_d(self):
        path = ROOT / "evidence/stage3-gold/pdp11-session.transcript.txt"
        if not path.exists():
            self.skipTest("native gold evidence not recorded")
        text = path.read_text(encoding="utf-8")
        self.assertIn("STAGE3-GOLD START=001000 EXPECT=D\nD\nHALT instruction", text)


if __name__ == "__main__":
    unittest.main()
