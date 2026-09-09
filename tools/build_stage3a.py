#!/usr/bin/env python3
"""Build fixed Stage 3A deposits using the class-M PDP-11 oracle."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pdp11_oracle import Operand, decode_one, encode


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "stage3a"
BOOTSTRAP_FIRST, BOOTSTRAP_LAST = 0o057744, 0o057776
MEMORY_BYTES = 24 * 1024
LABELS = {
    "start": 0o001000, "c": 0o001100, "x": 0o001120,
    "va": 0o001140, "b12": 0o001160, "b1": 0o001200,
    "emit": 0o001240, "stop": 0o001300,
    "stream_a": 0o002000, "stream_b": 0o002040,
    "stream_c": 0o002100, "stream_d": 0o002140,
    "external": 0o003000, "target": 0o003002,
    "frame": 0o004000, "stack": 0o005000,
}


@dataclass(frozen=True)
class PlacedWord:
    address: int
    word: int
    kind: str
    text: str


@dataclass(frozen=True)
class TestImage:
    name: str
    expected: str
    stream: int
    words: tuple[PlacedWord, ...]
    final_examine: tuple[int, ...]


class FixedBuilder:
    """Tiny fixed-layout emitter, deliberately not a general assembler."""

    def __init__(self) -> None:
        self.words: list[PlacedWord] = []

    def instruction(self, location: int, text: str, mnemonic: str, *operands, **kwargs) -> int:
        encoded = encode(mnemonic, *operands, **kwargs)
        decoded = decode_one(encoded, location)
        if decoded.mnemonic != mnemonic.upper():
            raise AssertionError(f"oracle decoded {decoded.mnemonic}, expected {mnemonic}")
        for offset, word in enumerate(encoded):
            kind = "instruction" if offset == 0 else "extension"
            self.words.append(PlacedWord(location + 2 * offset, word, kind, text))
        return location + 2 * len(encoded)

    def data(self, address: int, values: Iterable[int], text: str) -> None:
        for offset, word in enumerate(values):
            if not 0 <= word <= 0xFFFF:
                raise ValueError("data word must fit 16 bits")
            self.words.append(PlacedWord(address + 2 * offset, word, "thread/data", text))


def build_common(stream: int) -> list[PlacedWord]:
    b = FixedBuilder()
    pc = LABELS["start"]
    pc = b.instruction(pc, "mov #STREAM,r3", "MOV", Operand(2, 7, stream), Operand(0, 3))
    pc = b.instruction(pc, "mov #004000,r4", "MOV", Operand(2, 7, LABELS["frame"]), Operand(0, 4))
    pc = b.instruction(pc, "mov #005000,r5", "MOV", Operand(2, 7, LABELS["stack"]), Operand(0, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["c"]
    pc = b.instruction(pc, "mov (r3)+,(r5)+", "MOV", Operand(2, 3), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["x"]
    pc = b.instruction(pc, "mov @(r3)+,(r5)+", "MOV", Operand(3, 3), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["va"]
    pc = b.instruction(pc, "mov (r3)+,r0", "MOV", Operand(2, 3), Operand(0, 0))
    pc = b.instruction(pc, "add r4,r0", "ADD", Operand(0, 4), Operand(0, 0))
    pc = b.instruction(pc, "asr r0", "ASR", Operand(0, 0))
    pc = b.instruction(pc, "mov r0,(r5)+", "MOV", Operand(0, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["b12"]
    pc = b.instruction(pc, "add -(r5),-2(r5)", "ADD", Operand(4, 5), Operand(6, 5, 0o177776))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["b1"]
    pc = b.instruction(pc, "mov -(r5),r0", "MOV", Operand(4, 5), Operand(0, 0))
    pc = b.instruction(pc, "mov -(r5),r1", "MOV", Operand(4, 5), Operand(0, 1))
    pc = b.instruction(pc, "asl r1", "ASL", Operand(0, 1))
    pc = b.instruction(pc, "mov r0,(r1)", "MOV", Operand(0, 0), Operand(1, 1))
    pc = b.instruction(pc, "mov r0,(r5)+", "MOV", Operand(0, 0), Operand(2, 5))
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))

    pc = LABELS["emit"]
    pc = b.instruction(pc, "mov -(r5),r0", "MOV", Operand(4, 5), Operand(0, 0))
    poll = pc
    pc = b.instruction(pc, "tstb @#177564", "TSTB", Operand(3, 7, 0o177564))
    pc = b.instruction(pc, "bpl poll", "BPL", address=pc, target=poll)
    pc = b.instruction(pc, "movb r0,@#177566", "MOVB", Operand(0, 0), Operand(3, 7, 0o177566))
    drain = pc
    pc = b.instruction(pc, "tstb @#177564 (drain)", "TSTB", Operand(3, 7, 0o177564))
    pc = b.instruction(pc, "bpl drain", "BPL", address=pc, target=drain)
    b.instruction(pc, "jmp @(r3)+", "JMP", Operand(3, 3))
    b.instruction(LABELS["stop"], "halt", "HALT")
    return b.words


def build_images() -> dict[str, TestImage]:
    specs = {
        "a": ("A", "stream_a", [LABELS["c"], 0o0100, LABELS["c"], 1, LABELS["b12"], LABELS["emit"], LABELS["stop"]], ()),
        "b": ("B", "stream_b", [LABELS["x"], LABELS["external"], LABELS["emit"], LABELS["stop"]], ()),
        "c": ("C", "stream_c", [LABELS["c"], LABELS["target"] // 2, LABELS["c"], 0o0103, LABELS["b1"], LABELS["emit"], LABELS["stop"]], (LABELS["target"],)),
        "d": ("D", "stream_d", [LABELS["va"], 4, LABELS["c"], 0o0104, LABELS["b1"], LABELS["emit"], LABELS["stop"]], (LABELS["frame"] + 4,)),
    }
    images: dict[str, TestImage] = {}
    for name, (expected, stream_name, stream_words, examine) in specs.items():
        stream = LABELS[stream_name]
        common = build_common(stream)
        data = FixedBuilder()
        data.data(stream, stream_words, f"threaded stream {name.upper()}")
        if name == "b": data.data(LABELS["external"], [0o0102], "external value B")
        if name == "c": data.data(LABELS["target"], [0], "assignment target")
        if name == "d": data.data(LABELS["frame"], [0, 0, 0], "synthetic frame")
        words = tuple(sorted(common + data.words, key=lambda item: item.address))
        _validate_layout(words)
        images[name] = TestImage(name, expected, stream, words, examine)
    return images


def _validate_layout(words: tuple[PlacedWord, ...]) -> None:
    addresses = [item.address for item in words]
    if len(addresses) != len(set(addresses)):
        raise ValueError("overlapping generated words")
    for address in addresses:
        if address & 1 or not 0 <= address < MEMORY_BYTES:
            raise ValueError(f"address {address:06o} is outside aligned 24 KB memory")
        if BOOTSTRAP_FIRST <= address <= BOOTSTRAP_LAST:
            raise ValueError("generated word overlaps documented bootstrap")


def manifest(images: dict[str, TestImage]) -> str:
    lines = ["Stage 3A deterministic word manifest (M / modern instrumentation)",
             "All addresses and words are octal PDP-11 byte addresses/16-bit words.", ""]
    for name, image in images.items():
        lines.append(f"TEST {name.upper()} expected={image.expected} start={LABELS['start']:06o} stream={image.stream:06o}")
        lines.extend(f"{item.address:06o}\t{item.word:06o}\t{item.kind}\t{item.text}" for item in image.words)
        lines.append("")
    return "\n".join(lines)


def simh_script(image: TestImage) -> str:
    lines = ["; Stage 3A M-class deterministic deposit/run harness.",
             "; Uses baseline; no disk, tape attachment, UNIX, or KE11.",
             f"set log -n evidence/stage3a/test-{image.name}.transcript.txt",
             "do machines/pdp11/pdp11.simh"]
    lines.extend(f"dep {item.address:06o} {item.word:06o}" for item in image.words)
    lines.extend((f"echo STAGE3A-{image.name.upper()} START={LABELS['start']:06o} EXPECT={image.expected}",
                  f"go {LABELS['start']:06o}", "echo", f"echo STAGE3A-{image.name.upper()} HALTED",
                  "examine pc,r3,r4,r5"))
    lines.extend(f"examine {address:06o}" for address in image.final_examine)
    lines.extend(("show cpu", "show dev", "show ptr", "quit", ""))
    return "\n".join(lines)


def write_outputs() -> None:
    images = build_images()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.txt").write_text(manifest(images), encoding="ascii")
    for name, image in images.items():
        (OUT / f"test-{name}.simh").write_text(simh_script(image), encoding="ascii")


if __name__ == "__main__":
    write_outputs()
