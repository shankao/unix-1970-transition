#!/usr/bin/env python3
"""Host checks for Stage 4B artifacts; no host-side assembler semantics."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run_stage4b as runner  # noqa: E402


class Stage4BArtifacts(unittest.TestCase):
    def test_all_native_cases_have_fixed_vectors(self) -> None:
        self.assertEqual(set(runner.CASES), set(runner.EXPECTED_SHA256))

    def test_captured_native_outputs_match(self) -> None:
        for native, expected in runner.EXPECTED_SHA256.items():
            data = (ROOT / "evidence/stage4b" / f"{native}.out").read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected, native)

    def test_positive_fixture_crosses_input_buffer(self) -> None:
        self.assertGreater((ROOT / "tests/pdp7-as11/stage4b-positive.s").stat().st_size, 128)

    def test_substantial_fixture_measurement(self) -> None:
        text = (ROOT / "tests/pdp7-as11/stage4b-substantial.s").read_text()
        globals_ = set(re.findall(r"\b(?:a|s)[0-9][0-9](?=[:=])", text))
        locals_ = re.findall(r"(?m)(?<![A-Za-z0-9_])([0-9]):", text)
        self.assertEqual((len(globals_), len(locals_)), (48, 10))

    def test_compact_global_table_retains_packed_names(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertIn("017537-nglob*5", source)
        self.assertIn("nglob >= 48", source)
        self.assertIn("p[0]&0177777", source)

    def test_numeric_locals_are_separate_and_bounded(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertIn("017544+nlocal*2", source)
        self.assertIn("occ[10]", source)
        self.assertIn("nlocal >= 10", source)

    def test_real_internal_two_pass_rewind(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertRegex(source, r"pass = 1;[\s\S]*program\(\);[\s\S]*rewind\(\);[\s\S]*pass = 2;")

    def test_eight_character_packed_names(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertIn("if(i<8)", source)
        self.assertIn("p=i/2", source)
        self.assertNotIn("tolower", source)

    def test_location_is_byte_addressed(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertIn("loc=loc+2", source)
        self.assertIn("loc&1", source)
        self.assertIn("loc>0177776", source)

    def test_expression_surface_is_deliberately_small(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text()
        self.assertIn("ctab[12] '.','+','-','[',']'", source)
        self.assertIn("tok=i+5", source)

    def test_stage4c_extends_the_same_stage4b_source(self) -> None:
        source = (ROOT / "src/pdp7/as11/as11.b").read_text().lower()
        self.assertIn("stage 4c", source)
        self.assertIn("mfind", source)

    def test_stage3_symbol_demand_is_stable(self) -> None:
        sources = [
            ROOT / "src/pdp11/threaded-b/core.s",
            ROOT / "src/pdp11/threaded-b/control-call.s",
        ]
        globals_ = []
        locals_ = []
        for path in sources:
            text = path.read_text()
            globals_.extend(re.findall(r"(?m)^([a-z][a-z0-9]*):", text))
            locals_.extend(re.findall(r"(?m)^([0-9]):", text))
        self.assertEqual((len(globals_), len(locals_)), (17, 5))


if __name__ == "__main__":
    unittest.main()
