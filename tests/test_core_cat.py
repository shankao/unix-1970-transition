# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from dec_abs import parse_absolute, words_from_bytes
from run_core_cat import (
    CAT_SOURCE, CAT_TAPE, EVIDENCE, EXPECTED, NATIVE_STEMS, SYSTEM_SOURCES,
    SYSTEM_TAPES, labels_from_trace, validate_native,
)
from run_stage3_gold import parse_trace


class CoreUnixCatTests(unittest.TestCase):
    def test_sources_are_separate_and_cat_does_not_contain_file_text(self):
        system = "".join(
            source.read_text(encoding="ascii")
            for source in SYSTEM_SOURCES.values()
        )
        cat = CAT_SOURCE.read_text(encoding="ascii")
        self.assertIn("surviving pdp-7 s2/s4/s5/s6/s8", system.lower())
        self.assertIn("translation of the surviving PDP-7 cat", cat)
        self.assertIn("trap sxopen", cat)
        self.assertIn("trap sxread", cat)
        self.assertIn("trap sxwrite", cat)
        self.assertIn("trap sxclose", cat)
        self.assertIn("trap sxexit", cat)
        self.assertNotIn("PDP-11 Unix read this", cat)
        for absent in ("creat", "unlink", "stat", "fork", "shell"):
            self.assertIsNone(re.search(rf"\b{absent}\b", system.lower()))

    def test_recorded_native_words_and_tapes_match(self):
        if not all((EVIDENCE / f"{name}-native-trace.txt").exists()
                   for name in SYSTEM_SOURCES):
            self.skipTest("core cat native evidence not recorded")
        system_texts = {
            name: (EVIDENCE / f"{name}-native-trace.txt").read_text(
                encoding="ascii"
            ) for name in SYSTEM_SOURCES
        }
        system_text = "".join(system_texts.values())
        cat_text = (EVIDENCE / "cat-native-trace.txt").read_text(encoding="ascii")
        system, cat = parse_trace(system_text), parse_trace(cat_text)
        validate_native(system, cat, labels_from_trace(system_text))
        loads = tuple(
            (SYSTEM_TAPES[name], parse_trace(system_texts[name]))
            for name in SYSTEM_SOURCES
        ) + ((CAT_TAPE, cat),)
        for tape, records in loads:
            memory, transfer, _ = parse_absolute(tape.read_bytes())
            self.assertEqual({item.address: item.word for item in records},
                             words_from_bytes(memory))
            self.assertEqual(1, transfer)

    def test_recorded_runs_show_real_cat_result(self):
        if not (EVIDENCE / "fast-pdp11.transcript.txt").exists():
            self.skipTest("core cat execution evidence not recorded")
        for name in ("fast-pdp11.transcript.txt", "paper-tape-pdp11.transcript.txt"):
            text = (EVIDENCE / name).read_text(encoding="latin1").replace("\r", "")
            self.assertIn(EXPECTED.replace("\r", ""), text)
            self.assertIn("HALT instruction", text)

    def test_historical_load_deposits_only_the_bootstrap(self):
        source = (ROOT / "tools/run_core_cat.py").read_text(encoding="utf-8")
        historical = source.split("def historical_load", 1)[1].split(
            "def run", 1)[0]
        self.assertIn("for index, word in enumerate(BOOTSTRAP)", historical)
        self.assertNotIn("deposit {item.address", historical)
        self.assertIn("attach ptr", historical)
        self.assertIn("go 057500", historical)

    def test_transport_parser_accepts_assignment_metadata(self):
        self.assertEqual(1, len(parse_trace(
            "a sxopen 000002\ni 001000 000000\n"
        )))

    def test_normal_build_uses_a_disposable_era_disk(self):
        source = (ROOT / "tools/run_core_cat.py").read_text(encoding="utf-8")
        self.assertIn("TemporaryDirectory", source)
        self.assertIn("shutil.copy2(ERA / name", source)
        self.assertIn("for name in SYSTEM_SOURCES", source)
        self.assertIn('f"as11 {stem}.s {stem}.o"', source)
        self.assertIn('native.command("as11 ucat.s ucat.o"', source)
        self.assertIn('native.command(f"abspun {name} uxout"', source)
        self.assertTrue(all(len(f"{stem}.s") <= 8 and len(f"{stem}.o") <= 8
                            for stem in NATIVE_STEMS.values()))
        self.assertNotIn("from pdp11_oracle import encode", source)
        self.assertNotIn("def encode", source)


if __name__ == "__main__":
    unittest.main()
