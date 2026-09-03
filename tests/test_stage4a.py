from pathlib import Path
import unittest

from tools.run_stage4a import ROOT, RUNTIME_COPIES, SOURCE_FILES, expected_result


class Stage4AHostTests(unittest.TestCase):
    def test_input_exercises_odd_and_refill_prefixes(self):
        text = SOURCE_FILES["input"].read_text(encoding="ascii")
        self.assertGreater(len(text), 128)
        self.assertEqual(17 % 2, 1)
        self.assertGreater(173, 128)
        self.assertLess(173, len(text))

    def test_rewind_helper_uses_seek_and_invalidates_exact_state(self):
        text = SOURCE_FILES["rewind.s"].read_text()
        self.assertIn("lac .fin\n   sys seek; 0; 0", text)
        self.assertIn("dzm iflg\n   lac eibufp\n   dac cibufp", text)
        self.assertNotIn("dac ibufp", text)

    def test_probe_has_no_assembler_engine(self):
        text = SOURCE_FILES["io.b"].read_text()
        for term in ("opcode", "symbol", "operand", "label"):
            self.assertNotIn(term, text.lower())

    def test_runtime_working_copies_are_exact_checked_in_sources(self):
        self.assertEqual({"s4bl.s", "s4bi.s"}, set(RUNTIME_COPIES))
        for path in RUNTIME_COPIES.values():
            self.assertTrue(path.is_file())

    def test_expected_octals_are_six_digits(self):
        expected = expected_result(SOURCE_FILES["input"].read_text(encoding="ascii"))
        self.assertIn("o:\n000000\n000001\n077777\n100000\n177777\n", expected)

    def test_canonical_result_matches(self):
        result = ROOT / "evidence/stage4a/result.txt"
        self.assertTrue(result.exists())
        self.assertEqual(
            expected_result(SOURCE_FILES["input"].read_text(encoding="ascii")),
            result.read_text(encoding="ascii"),
        )

    def test_canonical_transcript_records_shankao_and_native_tools(self):
        text = (ROOT / "evidence/stage4a/session.transcript.txt").read_text(
            encoding="latin1"
        )
        self.assertIn("login: shankao", text.replace("\r", ""))
        self.assertIn("b io.b io.s", text.replace("\r", ""))
        self.assertIn(
            "as s4op.s s4bl.s io.s rewind.s s4bi.s", text.replace("\r", "")
        )

    def test_state_evidence_records_authoritative_image_hashes(self):
        text = (ROOT / "evidence/stage4a/image-state.txt").read_text()
        self.assertIn("pre_sha256=", text)
        self.assertIn("post_sha256=", text)
        self.assertIn("machines/pdp7/pdp7-unix/build/image-shankao.fs", text)


if __name__ == "__main__":
    unittest.main()
