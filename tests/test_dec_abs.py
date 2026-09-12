# SPDX-License-Identifier: GPL-3.0-only
import unittest

from tools.dec_abs import parse_absolute, words_from_bytes


def record(address: int, data: bytes) -> bytes:
    body = bytes((1, 0, len(data) + 6, 0, address & 255, address >> 8)) + data
    return body + bytes((-sum(body) & 255,))


class DecAbsoluteTapeTests(unittest.TestCase):
    def test_parse_little_endian_record_and_transfer(self):
        tape = b"\0\0" + record(0o1000, b"\x34\x12") + record(1, b"") + b"\0"
        memory, transfer, count = parse_absolute(tape)
        self.assertEqual(words_from_bytes(memory), {0o1000: 0o011064})
        self.assertEqual(transfer, 1)
        self.assertEqual(count, 2)

    def test_bad_checksum_rejected(self):
        tape = bytearray(record(0o1000, b"\x34\x12"))
        tape[-1] ^= 1
        with self.assertRaisesRegex(ValueError, "checksum"):
            parse_absolute(bytes(tape))

    def test_truncated_and_duplicate_records_rejected(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            parse_absolute(record(0o1000, b"x")[:-1])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            parse_absolute(record(0o1000, b"x") + record(0o1000, b"y"))


if __name__ == "__main__":
    unittest.main()
