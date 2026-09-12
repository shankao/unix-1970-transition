# SPDX-License-Identifier: GPL-3.0-only
"""Reference parsing for DEC PDP-11 absolute-binary paper tapes.

This class-M module validates tapes.  It is never the acceptance-tape producer.
"""

from __future__ import annotations

import re
from pathlib import Path


def loader_bytes(path: Path) -> bytes:
    """Decode PCjs's lossless word packing of DEC-11-L2PC-PO tape bytes."""
    text = path.read_text(encoding="ascii")
    words = [int(value, 16) for value in re.findall(r"0x([0-9A-Fa-f]{4})", text)]
    if not words:
        raise ValueError("loader archive contains no packed words")
    result = bytearray()
    for word in words:
        result.extend((word & 0xff, word >> 8))
    return bytes(result)


def parse_absolute(tape: bytes) -> tuple[dict[int, int], int | None, int]:
    """Return byte map, transfer address, and record count; reject bad input."""
    pos = 0
    while pos < len(tape) and tape[pos] == 0:
        pos += 1
    memory: dict[int, int] = {}
    transfer = None
    records = 0
    while pos < len(tape):
        if all(value == 0 for value in tape[pos:]):
            break
        if pos + 7 > len(tape):
            raise ValueError("truncated absolute record header")
        if tape[pos:pos + 2] != b"\x01\x00":
            raise ValueError(f"bad absolute signature at byte {pos}")
        count = tape[pos + 2] | tape[pos + 3] << 8
        address = tape[pos + 4] | tape[pos + 5] << 8
        if count < 6:
            raise ValueError("absolute record count is smaller than its header")
        end = pos + count + 1
        if end > len(tape):
            raise ValueError("truncated absolute record")
        block = tape[pos:end]
        if sum(block) & 0xff:
            raise ValueError(f"bad absolute checksum in record {records + 1}")
        data = block[6:-1]
        if data:
            for offset, value in enumerate(data):
                target = address + offset
                if target in memory:
                    raise ValueError(f"duplicate absolute byte at {target:06o}")
                memory[target] = value
        else:
            transfer = address
        records += 1
        pos = end
    if not records:
        raise ValueError("absolute tape has no records")
    return memory, transfer, records


def words_from_bytes(memory: dict[int, int]) -> dict[int, int]:
    if any(address & 1 and address - 1 not in memory for address in memory):
        raise ValueError("unpaired absolute data byte")
    words: dict[int, int] = {}
    for address in sorted(memory):
        if address & 1:
            continue
        if address + 1 not in memory:
            raise ValueError(f"missing high byte at {address:06o}")
        words[address] = memory[address] | memory[address + 1] << 8
    return words
