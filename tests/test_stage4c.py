import ast
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import pdp11_oracle as oracle


AS11 = (ROOT / "src/pdp7/as11/as11.b").read_text(encoding="ascii")
FIXTURE = (ROOT / "tests/pdp7-as11/stage4c-encoding.s").read_text(encoding="ascii")
EXPECTED = (ROOT / "tests/pdp7-as11/stage4c-encoding.expected").read_text(encoding="ascii")


class Stage4CHostTests(unittest.TestCase):
    def test_local_stage3_inventory_is_exact(self):
        found = set()
        for name in ("build_stage3a.py", "build_stage3b.py"):
            tree = ast.parse((ROOT / "tools" / name).read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (isinstance(node, ast.Call) and
                        isinstance(node.func, ast.Attribute) and
                        node.func.attr == "instruction" and len(node.args) >= 3):
                    try:
                        found.add(ast.literal_eval(node.args[2]).lower())
                    except (ValueError, TypeError):
                        pass
        self.assertEqual(
            {"add", "asl", "asr", "bne", "bpl", "br", "clr", "cmp",
             "halt", "jmp", "mov", "movb", "tst", "tstb"}, found
        )

    def test_fixed_trace_instructions_decode_with_stage2_oracle(self):
        records = []
        current = None
        for line in EXPECTED.splitlines():
            kind, address, value, *rest = line.split()
            if kind == "i":
                if current:
                    records.append(current)
                current = [int(address, 8), [int(value, 8)]]
            elif kind == "x":
                self.assertIsNotNone(current)
                expected_address = current[0] + 2 * len(current[1])
                self.assertEqual(expected_address, int(address, 8))
                current[1].append(int(value, 8))
            elif current:
                records.append(current)
                current = None
        if current:
            records.append(current)
        decoded = [oracle.decode_one(words, address) for address, words in records]
        self.assertTrue(all(len(item.words) == len(words)
                            for item, (_, words) in zip(decoded, records)))
        self.assertEqual(30, len(decoded))

    def test_pc_relative_extension_bases_and_order_are_fixed(self):
        rows = {int(a, 8): int(v, 8) for k, a, v in
                (line.split() for line in EXPECTED.splitlines()) if k == "x"}
        self.assertEqual(0o60, rows[0o1042])   # target - (source E + 2)
        self.assertEqual(0o54, rows[0o1046])
        self.assertEqual(0o50, rows[0o1052])  # source extension base
        self.assertEqual(0o50, rows[0o1054])  # destination's later base
        self.assertEqual(0o101, rows[0o1060])
        self.assertEqual(0o177566, rows[0o1062])

    def test_branch_boundaries_are_oracle_vectors(self):
        self.assertEqual([0o000577], oracle.encode("BR", address=0o2000, target=0o2400))
        self.assertEqual([0o000600], oracle.encode("BR", address=0o2400, target=0o2002))
        with self.assertRaises(oracle.OracleError):
            oracle.encode("BR", address=0o1000, target=0o400)
        with self.assertRaises(oracle.OracleError):
            oracle.encode("BR", address=0o1000, target=0o1402)

    def test_fixture_covers_modes_pc_forms_and_bootstrap_mnemonics(self):
        for text in ("r0", "(r0)", "(r0)+", "*(r0)+", "-(r0)",
                     "*-(r0)", "2(r0)", "*6(r0)", "$1", "*$177566",
                     "target,r0", "*target,r0"):
            self.assertIn(text, FIXTURE)
        for mnemonic in ("mov", "movb", "cmp", "add", "clr", "tst",
                         "tstb", "asl", "asr", "jmp", "jsr", "rts",
                         "br", "bne", "bpl", "halt"):
            self.assertIn(mnemonic, FIXTURE)

    def test_tables_and_stage4b_contract_remain_compact(self):
        self.assertIn("017537-nglob*5", AS11)
        self.assertIn("017544+nlocal*2", AS11)
        self.assertIn("rewind();", AS11)
        self.assertIn("outcode('w ',loc,v&0177777)", AS11)
        self.assertIn("ctab[12]", AS11)
        self.assertIn("'[',']'", AS11)
        self.assertIn("nglob >= 48", AS11)  # no premature 38-global guard

    def test_native_completion_readme_records_open_capacity_work(self):
        text = (ROOT / "src/pdp7/as11/readme.stage4c").read_text()
        self.assertIn("stage 4c", text)
        self.assertIn("ka11 instruction encoding", text)
        self.assertIn("final as11 memory capacity is not fixed yet", text)
        self.assertIn("stage 4d", text)

    def test_later_instructions_are_not_mnemonics(self):
        for name in ("mul", "div", "ash", "ashc", "xor", "sob", "mark"):
            self.assertNotIn("mneq(n,'" + "','".join(name), AS11)
        self.assertIn("mark:\nmark\n", FIXTURE)

    def test_runner_is_instrumentation_not_an_encoder(self):
        runner = (ROOT / "tools/run_stage4c.py").read_text(encoding="utf-8")
        self.assertNotIn("def encode", runner)
        self.assertIn('session.command("b as11.b as11.s"', runner)
        self.assertIn('session.command(f"a.out {native} {out}"', runner)


if __name__ == "__main__":
    unittest.main()
