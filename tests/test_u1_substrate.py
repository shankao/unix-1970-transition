from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from run_stage3_gold import parse_trace
from run_u1_substrate import (
    EVIDENCE, INT_ARTIFACT, RAM_ARTIFACT, labels_from_trace,
    simh_script, validate_interrupt, validate_ram,
)


class U1SubstrateTests(unittest.TestCase):
    def test_fixtures_are_readable_and_bounded(self):
        interrupt = (ROOT / "tests/pdp7-as11/u1-interrupt.s").read_text()
        ram = (ROOT / "tests/pdp7-as11/u1-ram.s").read_text()
        for phrase in ("low-core words", "receiver isr", "tx interrupt",
                       "trap frame pc"):
            self.assertIn(phrase, interrupt)
        for phrase in ("dynamic block", "512-byte", "process-backing"):
            self.assertIn(phrase, ram)
        self.assertNotIn("tstb *$177560", interrupt)
        self.assertNotIn("tstb *$177564", interrupt)
        for forbidden in ("inode", "namei", "fork", "sys open"):
            self.assertNotIn(forbidden, ram)

    def test_recorded_native_traces_pass_oracle_contract(self):
        int_trace = (EVIDENCE / "interrupt-native-trace.txt").read_text()
        ram_trace = (EVIDENCE / "ram-native-trace.txt").read_text()
        int_records = parse_trace(int_trace)
        ram_records = parse_trace(ram_trace)
        validate_interrupt(int_records, labels_from_trace(int_trace))
        validate_ram(ram_records)
        self.assertEqual(342, len(int_records) + len(ram_records))

    def test_artifacts_are_exact_native_deposit_maps(self):
        pairs = (
            ("interrupt-native-trace.txt", INT_ARTIFACT,
             "U1 INTERRUPT READY - TYPE 2 CHARACTERS"),
            ("ram-native-trace.txt", RAM_ARTIFACT, "U1 RAM STORAGE START"),
        )
        for trace_name, artifact, title in pairs:
            records = parse_trace((EVIDENCE / trace_name).read_text())
            self.assertEqual(simh_script(records, title), artifact.read_text())
            deposits = {
                tuple(int(value, 8) for value in line.split()[1:])
                for line in artifact.read_text().splitlines()
                if line.startswith("dep ")
            }
            self.assertEqual({(r.address, r.word) for r in records}, deposits)

    def test_runner_cannot_encode_execution_words(self):
        runner = (ROOT / "tools/run_u1_substrate.py").read_text()
        self.assertNotIn("from pdp11_oracle import encode", runner)
        self.assertNotIn("def encode", runner)
        self.assertIn("assemble_source_on_pdp7", runner)
        self.assertIn('child.send("A")', runner)
        self.assertIn('child.send("B")', runner)

    def test_recorded_execution_reached_both_pass_states(self):
        interrupt = (EVIDENCE / "interrupt-pdp11.transcript.txt").read_text(
            encoding="latin1")
        ram = (EVIDENCE / "ram-pdp11.transcript.txt").read_text(
            encoding="latin1")
        self.assertIn("AB\nHALT instruction", interrupt.replace("\r", ""))
        self.assertIn("U1 RAM STORAGE START", ram)
        self.assertIn("HALT instruction", ram)


if __name__ == "__main__":
    unittest.main()
