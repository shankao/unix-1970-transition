from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_kl11_poll import ARTIFACT, EXPECTED, manual_script, validate
from run_stage3_gold import parse_trace


class KL11PollingTests(unittest.TestCase):
    def test_fixture_is_commented_and_uses_only_stage4c_surface(self):
        source = (ROOT / "tests/pdp7-as11/kl11-poll.s").read_text()
        for phrase in ("receiver done", "tstb plus bpl", "save it in ram",
                       "transmitter buffer", "second input", "stop cleanly"):
            self.assertIn(phrase, source)
        for address in ("177560", "177562", "177564", "177566"):
            self.assertIn(address, source)
        for forbidden in ("rti", "trap", "sys ", ".byte"):
            self.assertNotIn(forbidden, source)

    def test_recorded_trace_decodes_to_exact_contract(self):
        path = ROOT / "evidence/kl11-poll/native-trace.txt"
        if not path.exists():
            self.skipTest("native KL11 evidence not recorded")
        validate(parse_trace(path.read_text(encoding="ascii")))
        self.assertEqual(19, len(EXPECTED))

    def test_manual_artifact_deposits_only_native_trace(self):
        path = ROOT / "evidence/kl11-poll/native-trace.txt"
        if not path.exists() or not ARTIFACT.exists():
            self.skipTest("native KL11 artifact not recorded")
        records = parse_trace(path.read_text(encoding="ascii"))
        self.assertEqual(manual_script(records), ARTIFACT.read_text(encoding="ascii"))
        deposits = {
            tuple(int(value, 8) for value in line.split()[1:])
            for line in ARTIFACT.read_text().splitlines() if line.startswith("dep ")
        }
        self.assertEqual({(item.address, item.word) for item in records}, deposits)

    def test_runner_has_no_host_encoder(self):
        runner = (ROOT / "tools/run_kl11_poll.py").read_text()
        self.assertNotIn("from pdp11_oracle import encode", runner)
        self.assertNotIn("def encode", runner)
        self.assertIn('assemble_source_on_pdp7(SOURCE, "klpoll"', runner)
        self.assertIn('child.send("A")', runner)
        self.assertIn('child.send("B")', runner)

    def test_recorded_run_echoes_and_saves_both_bytes(self):
        path = ROOT / "evidence/kl11-poll/pdp11-session.transcript.txt"
        if not path.exists():
            self.skipTest("native KL11 execution evidence not recorded")
        text = path.read_text(encoding="latin1")
        self.assertIn("KL11-POLL READY EXPECT=AB", text)
        self.assertIn("AB\nHALT instruction", text.replace("\r", ""))
        self.assertIn("1100:\t000101", text)
        self.assertIn("1102:\t000102", text)


if __name__ == "__main__":
    unittest.main()
