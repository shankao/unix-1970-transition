import importlib.util
from pathlib import Path
import sys
import unittest


MODULE_PATH = Path(__file__).parents[1] / "tools" / "pdp11_oracle.py"
SPEC = importlib.util.spec_from_file_location("pdp11_oracle", MODULE_PATH)
oracle = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = oracle
SPEC.loader.exec_module(oracle)

Operand = oracle.Operand


class OracleVectors(unittest.TestCase):
    def assertEncoding(self, expected, mnemonic, *operands, **kwargs):
        self.assertEqual(expected, oracle.encode(mnemonic, *operands, **kwargs))
        decoded = oracle.decode_one(expected, kwargs.get("address", 0))
        self.assertEqual(mnemonic, decoded.mnemonic)
        self.assertEqual(tuple(expected), decoded.words)

    def test_operand_specifiers_all_modes(self):
        for mode in range(8):
            for register in range(8):
                specifier = (mode << 3) | register
                self.assertEqual(specifier, oracle.encode_specifier(mode, register))
                self.assertEqual((mode, register), oracle.decode_specifier(specifier))

    def test_all_addressing_modes_decode_with_extensions(self):
        expected = ("R3", "(R3)", "(R3)+", "@(R3)+", "-(R3)",
                    "@-(R3)", "000012(R3)", "@000012(R3)")
        for mode, display in enumerate(expected):
            extension = 0o12 if mode in (6, 7) else None
            encoded = oracle.encode("MOV", Operand(mode, 3, extension), Operand(0, 0))
            self.assertEqual(display, oracle.decode_one(encoded).operands[0])
        pc_expected = ("#000012", "@#000012", "000016", "@000016")
        for mode, display in zip((2, 3, 6, 7), pc_expected):
            encoded = oracle.encode("MOV", Operand(mode, 7, 0o12), Operand(0, 0))
            self.assertEqual(display, oracle.decode_one(encoded).operands[0])

    def test_supplied_double_operand_vectors(self):
        vectors = [
            ([0o010001], "MOV", Operand(0, 0), Operand(0, 1)),
            ([0o012700, 0o000001], "MOV", Operand(2, 7, 1), Operand(0, 0)),
            ([0o010046], "MOV", Operand(0, 0), Operand(4, 6)),
            ([0o012600], "MOV", Operand(2, 6), Operand(0, 0)),
            ([0o112321], "MOVB", Operand(2, 3), Operand(2, 1)),
            ([0o110037, 0o177566], "MOVB", Operand(0, 0), Operand(3, 7, 0o177566)),
            ([0o020203], "CMP", Operand(0, 2), Operand(0, 3)),
            ([0o022525], "CMP", Operand(2, 5), Operand(2, 5)),
            ([0o060001], "ADD", Operand(0, 0), Operand(0, 1)),
            ([0o160203], "SUB", Operand(0, 2), Operand(0, 3)),
            ([0o032700, 1], "BIT", Operand(2, 7, 1), Operand(0, 0)),
            ([0o040001], "BIC", Operand(0, 0), Operand(0, 1)),
            ([0o050001], "BIS", Operand(0, 0), Operand(0, 1)),
        ]
        for expected, mnemonic, src, dst in vectors:
            with self.subTest(mnemonic=mnemonic, expected=expected):
                self.assertEncoding(expected, mnemonic, src, dst)

    def test_supplied_single_and_control_vectors(self):
        vectors = [
            ([0o005000], "CLR", Operand(0, 0)),
            ([0o005202], "INC", Operand(0, 2)),
            ([0o005303], "DEC", Operand(0, 3)),
            ([0o005404], "NEG", Operand(0, 4)),
            ([0o005700], "TST", Operand(0, 0)),
            ([0o006001], "ROR", Operand(0, 1)),
            ([0o006101], "ROL", Operand(0, 1)),
            ([0o006201], "ASR", Operand(0, 1)),
            ([0o006301], "ASL", Operand(0, 1)),
            ([0o105737, 0o177564], "TSTB", Operand(3, 7, 0o177564)),
            ([0o000133], "JMP", Operand(3, 3)),
        ]
        for expected, mnemonic, operand in vectors:
            with self.subTest(mnemonic=mnemonic):
                self.assertEncoding(expected, mnemonic, operand)
        self.assertEncoding([0o004567, 0o000020], "JSR", 5, Operand(6, 7, 0o20))
        self.assertEncoding([0o000205], "RTS", 5)
        self.assertEncoding([0o000207], "RTS", 7)
        self.assertEncoding([0o000000], "HALT")

    def test_all_supported_names_encode_and_decode(self):
        for mnemonic in oracle.DOUBLE:
            self.assertEncoding(oracle.encode(mnemonic, Operand(0, 0), Operand(0, 1)), mnemonic, Operand(0, 0), Operand(0, 1))
        for mnemonic in oracle.SINGLE:
            self.assertEncoding(oracle.encode(mnemonic, Operand(0, 0)), mnemonic, Operand(0, 0))
        for mnemonic in oracle.FIXED:
            self.assertEncoding(oracle.encode(mnemonic), mnemonic)
        for mnemonic in oracle.TRAPS:
            self.assertEncoding(oracle.encode(mnemonic, 0o123), mnemonic, 0o123)
        for mnemonic in oracle.BRANCH:
            encoded = oracle.encode(mnemonic, address=0o1000, target=0o1004)
            self.assertEqual(encoded, oracle.encode(mnemonic, address=0o1000, target=0o1004))
            self.assertEqual(0o1004, int(oracle.decode_one(encoded, 0o1000).operands[0], 8))

    def test_branch_vectors_and_inverse(self):
        self.assertEncoding([0o000403], "BR", address=0o001000, target=0o001010)
        self.assertEncoding([0o000777], "BR", address=0o001000, target=0o001000)
        self.assertEqual([0o001002], oracle.encode("BNE", address=0o001000, target=0o001006))
        for displacement in (-128, -1, 0, 1, 127):
            address = 0o001000
            target = address + 2 + 2 * displacement
            encoded = oracle.branch_displacement(address, target)
            self.assertEqual(target, oracle.branch_target(address, encoded))

    def test_dec_handbook_cmpb_gold_vector(self):
        expected = [0o123727, 0o177560, 0o000301]
        actual = oracle.encode("CMPB", Operand(3, 7, 0o177560), Operand(2, 7, 0o301))
        self.assertEqual(expected, actual)
        decoded = oracle.decode_one(actual, 0o001000)
        self.assertEqual(("@#177560", "#000301"), decoded.operands)
        self.assertEqual(tuple(expected), decoded.words)

    def test_little_endian_serialization(self):
        self.assertEqual(bytes((0xC0, 0x15)), oracle.words_to_bytes([0o012700]))
        self.assertEqual(bytes((0x76, 0xFF)), oracle.words_to_bytes([0o177566]))

    def test_pc_special_and_indexed_display(self):
        instruction = oracle.decode_one([0o016701, 0o000026], 0o057744)
        self.assertEqual(("057776", "R1"), instruction.operands)
        self.assertEqual("MOV", instruction.mnemonic)
        absolute = oracle.decode_one([0o110037, 0o177566])
        self.assertEqual(("R0", "@#177566"), absolute.operands)

    def test_bootstrap_regression_stream(self):
        words = [
            0o016701, 0o000026, 0o012702, 0o000352, 0o005211,
            0o105711, 0o100376, 0o116162, 0o000002, 0o057400,
            0o005267, 0o177756, 0o000765, 0o177550,
        ]
        decoded = oracle.decode_stream(words[:-1], 0o057744)
        self.assertEqual(["MOV", "MOV", "INC", "TSTB", "BPL", "MOVB", "INC", "BR"], [item.mnemonic for item in decoded])
        self.assertEqual((0o116162, 0o000002, 0o057400), decoded[5].words)
        self.assertEqual("057756", decoded[4].operands[0])
        self.assertEqual("057750", decoded[7].operands[0])
        self.assertEqual(0o177550, words[-1])  # data, deliberately not decoded


class OracleNegativeTests(unittest.TestCase):
    def test_bad_branch_targets(self):
        with self.assertRaises(oracle.OracleError):
            oracle.branch_displacement(0o1000, 0o1003)
        with self.assertRaises(oracle.OracleError):
            oracle.branch_displacement(0o1000, 0o1002 + 2 * 128)
        with self.assertRaises(oracle.OracleError):
            oracle.branch_displacement(0o1000, 0o1002 - 2 * 129)

    def test_bad_operand_fields(self):
        with self.assertRaises(oracle.OracleError):
            oracle.encode_specifier(8, 0)
        with self.assertRaises(oracle.OracleError):
            oracle.encode_specifier(0, 8)
        with self.assertRaises(oracle.OracleError):
            Operand(6, 0)
        with self.assertRaises(oracle.OracleError):
            Operand(0, 0, 1)

    def test_later_instructions_are_unsupported(self):
        words = {"MUL": 0o070000, "DIV": 0o071000, "ASH": 0o072000,
                 "ASHC": 0o073000, "XOR": 0o074000, "SOB": 0o077000}
        for mnemonic, word in words.items():
            with self.subTest(mnemonic=mnemonic):
                with self.assertRaises(oracle.UnsupportedInstruction):
                    oracle.encode(mnemonic)
                with self.assertRaises(oracle.UnsupportedInstruction):
                    oracle.decode_one([word])


if __name__ == "__main__":
    unittest.main()
