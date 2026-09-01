#!/usr/bin/env python3
"""Class-M PDP-11/20 instruction encoding and decoding oracle."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable, Sequence


class OracleError(ValueError):
    """Base error for invalid or unsupported oracle input."""


class UnsupportedInstruction(OracleError):
    """Instruction is outside the project's base KA11 target."""


REG_NAMES = ("R0", "R1", "R2", "R3", "R4", "R5", "SP", "PC")

DOUBLE = {
    "MOV": 0o010000, "CMP": 0o020000, "BIT": 0o030000,
    "BIC": 0o040000, "BIS": 0o050000, "ADD": 0o060000,
    "MOVB": 0o110000, "CMPB": 0o120000, "BITB": 0o130000,
    "BICB": 0o140000, "BISB": 0o150000, "SUB": 0o160000,
}
SINGLE = {
    "JMP": 0o000100, "SWAB": 0o000300,
    "CLR": 0o005000, "COM": 0o005100, "INC": 0o005200,
    "DEC": 0o005300, "NEG": 0o005400, "ADC": 0o005500,
    "SBC": 0o005600, "TST": 0o005700, "ROR": 0o006000,
    "ROL": 0o006100, "ASR": 0o006200, "ASL": 0o006300,
    "CLRB": 0o105000, "COMB": 0o105100, "INCB": 0o105200,
    "DECB": 0o105300, "NEGB": 0o105400, "ADCB": 0o105500,
    "SBCB": 0o105600, "TSTB": 0o105700, "RORB": 0o106000,
    "ROLB": 0o106100, "ASRB": 0o106200, "ASLB": 0o106300,
}
BRANCH = {
    "BR": 0o000400, "BNE": 0o001000, "BEQ": 0o001400,
    "BGE": 0o002000, "BLT": 0o002400, "BGT": 0o003000,
    "BLE": 0o003400, "BPL": 0o100000, "BMI": 0o100400,
    "BHI": 0o101000, "BLOS": 0o101400, "BVC": 0o102000,
    "BVS": 0o102400, "BCC": 0o103000, "BHIS": 0o103000,
    "BCS": 0o103400, "BLO": 0o103400,
}
FIXED = {
    "HALT": 0o000000, "WAIT": 0o000001, "RTI": 0o000002,
    "IOT": 0o000004, "RESET": 0o000005, "CLC": 0o000241,
    "SEC": 0o000261,
}
TRAPS = {"EMT": 0o104000, "TRAP": 0o104400}
UNSUPPORTED = {"MUL", "DIV", "ASH", "ASHC", "SOB", "XOR"}
UNSUPPORTED_PATTERNS = (
    (0o177000, 0o070000, "MUL"), (0o177000, 0o071000, "DIV"),
    (0o177000, 0o072000, "ASH"), (0o177000, 0o073000, "ASHC"),
    (0o177000, 0o074000, "XOR"), (0o177000, 0o077000, "SOB"),
)


def _word(value: int, what: str = "word") -> int:
    if not isinstance(value, int) or not 0 <= value <= 0xFFFF:
        raise OracleError(f"{what} must fit 16 bits")
    return value


@dataclass(frozen=True)
class Operand:
    mode: int
    register: int
    extension: int | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.mode <= 7:
            raise OracleError("addressing mode must be in range 0..7")
        if not 0 <= self.register <= 7:
            raise OracleError("register must be in range 0..7")
        needs_extension = self.mode in (6, 7) or (
            self.register == 7 and self.mode in (2, 3)
        )
        if needs_extension != (self.extension is not None):
            requirement = "requires" if needs_extension else "does not take"
            raise OracleError(f"mode {self.mode}, register {self.register} {requirement} an extension word")
        if self.extension is not None:
            _word(self.extension, "extension")

    @property
    def specifier(self) -> int:
        return encode_specifier(self.mode, self.register)


@dataclass(frozen=True)
class DecodedInstruction:
    address: int
    mnemonic: str
    operands: tuple[str, ...]
    words: tuple[int, ...]

    def __str__(self) -> str:
        args = ",".join(self.operands)
        return f"{self.address:06o}: " + " ".join(f"{w:06o}" for w in self.words) + f"  {self.mnemonic}" + (f" {args}" if args else "")


def encode_specifier(mode: int, register: int) -> int:
    if not isinstance(mode, int) or not 0 <= mode <= 7:
        raise OracleError("addressing mode must be in range 0..7")
    if not isinstance(register, int) or not 0 <= register <= 7:
        raise OracleError("register must be in range 0..7")
    return (mode << 3) | register


def decode_specifier(specifier: int) -> tuple[int, int]:
    if not isinstance(specifier, int) or not 0 <= specifier <= 0o77:
        raise OracleError("operand specifier must be in range 00..77 octal")
    return specifier >> 3, specifier & 7


def branch_displacement(instruction_address: int, target: int) -> int:
    _word(instruction_address, "instruction address")
    _word(target, "target address")
    delta = target - (instruction_address + 2)
    if delta & 1:
        raise OracleError("branch target displacement must be word-aligned")
    displacement = delta // 2
    if not -128 <= displacement <= 127:
        raise OracleError("branch displacement is outside signed 8-bit range")
    return displacement & 0xFF


def branch_target(instruction_address: int, encoded_displacement: int) -> int:
    _word(instruction_address, "instruction address")
    if not isinstance(encoded_displacement, int) or not 0 <= encoded_displacement <= 0xFF:
        raise OracleError("encoded branch displacement must fit 8 bits")
    signed = encoded_displacement - 256 if encoded_displacement & 0x80 else encoded_displacement
    target = instruction_address + 2 + 2 * signed
    return _word(target, "decoded branch target")


def encode(mnemonic: str, *operands: Operand | int, address: int | None = None, target: int | None = None) -> list[int]:
    name = mnemonic.upper()
    if name in UNSUPPORTED:
        raise UnsupportedInstruction(f"{name} is outside the base KA11/11/20 project target")
    if name in DOUBLE:
        if len(operands) != 2 or not all(isinstance(op, Operand) for op in operands):
            raise OracleError(f"{name} requires two Operand values")
        src, dst = operands
        assert isinstance(src, Operand) and isinstance(dst, Operand)
        return [DOUBLE[name] | (src.specifier << 6) | dst.specifier] + _extensions(src, dst)
    if name in SINGLE:
        if len(operands) != 1 or not isinstance(operands[0], Operand):
            raise OracleError(f"{name} requires one Operand")
        op = operands[0]
        return [SINGLE[name] | op.specifier] + _extensions(op)
    if name in BRANCH:
        if operands:
            raise OracleError(f"{name} uses address= and target=, not operands")
        if address is None or target is None:
            raise OracleError(f"{name} requires address and target")
        return [BRANCH[name] | branch_displacement(address, target)]
    if name == "JSR":
        if len(operands) != 2 or not isinstance(operands[0], int) or not isinstance(operands[1], Operand):
            raise OracleError("JSR requires register number and destination Operand")
        register, dst = operands
        if not 0 <= register <= 7:
            raise OracleError("register must be in range 0..7")
        return [0o004000 | (register << 6) | dst.specifier] + _extensions(dst)
    if name == "RTS":
        if len(operands) != 1 or not isinstance(operands[0], int) or not 0 <= operands[0] <= 7:
            raise OracleError("RTS requires a register in range 0..7")
        return [0o000200 | operands[0]]
    if name in FIXED:
        if operands:
            raise OracleError(f"{name} takes no operands")
        return [FIXED[name]]
    if name in TRAPS:
        if len(operands) != 1 or not isinstance(operands[0], int) or not 0 <= operands[0] <= 0xFF:
            raise OracleError(f"{name} requires an 8-bit vector")
        return [TRAPS[name] | operands[0]]
    raise UnsupportedInstruction(f"unsupported instruction {name}")


def _extensions(*operands: Operand) -> list[int]:
    return [op.extension for op in operands if op.extension is not None]  # type: ignore[misc]


def words_to_bytes(words: Iterable[int]) -> bytes:
    result = bytearray()
    for value in words:
        word = _word(value)
        result.extend((word & 0xFF, word >> 8))
    return bytes(result)


def _take_operand(specifier: int, words: Sequence[int], index: int, extension_address: int) -> tuple[str, int]:
    mode, register = decode_specifier(specifier)
    extension = None
    if mode in (6, 7) or (register == 7 and mode in (2, 3)):
        if index >= len(words):
            raise OracleError("instruction is missing an extension word")
        extension = _word(words[index], "extension")
        index += 1
    name = REG_NAMES[register]
    if register == 7 and mode == 2:
        text = f"#{extension:06o}"
    elif register == 7 and mode == 3:
        text = f"@#{extension:06o}"
    elif register == 7 and mode in (6, 7):
        assert extension is not None
        signed = extension - 0x10000 if extension & 0x8000 else extension
        target = (extension_address + 2 + signed) & 0xFFFF
        text = ("@" if mode == 7 else "") + f"{target:06o}"
    elif mode == 0:
        text = name
    elif mode == 1:
        text = f"({name})"
    elif mode == 2:
        text = f"({name})+"
    elif mode == 3:
        text = f"@({name})+"
    elif mode == 4:
        text = f"-({name})"
    elif mode == 5:
        text = f"@-({name})"
    else:
        assert extension is not None
        text = ("@" if mode == 7 else "") + f"{extension:06o}({name})"
    return text, index


def decode_one(words: Sequence[int], address: int = 0) -> DecodedInstruction:
    if not words:
        raise OracleError("no instruction word supplied")
    _word(address, "instruction address")
    word = _word(words[0])
    for mask, value, name in UNSUPPORTED_PATTERNS:
        if word & mask == value:
            raise UnsupportedInstruction(f"{name} word is outside the base KA11/11/20 project target")
    index = 1
    operands: list[str] = []
    mnemonic = ""
    double_base = word & 0o170000
    reverse_double = {value: name for name, value in DOUBLE.items()}
    if double_base in reverse_double:
        mnemonic = reverse_double[double_base]
        src, index = _take_operand((word >> 6) & 0o77, words, index, address + 2 * index)
        dst, index = _take_operand(word & 0o77, words, index, address + 2 * index)
        operands = [src, dst]
    elif word & 0o177400 in set(BRANCH.values()):
        canonical = {value: name for name, value in BRANCH.items() if name not in ("BHIS", "BLO")}
        mnemonic = canonical[word & 0o177400]
        operands = [f"{branch_target(address, word & 0xFF):06o}"]
    elif word & 0o177000 == 0o004000:
        mnemonic = "JSR"
        operands.append(REG_NAMES[(word >> 6) & 7])
        dst, index = _take_operand(word & 0o77, words, index, address + 2 * index)
        operands.append(dst)
    elif word & 0o177770 == 0o000200:
        mnemonic, operands = "RTS", [REG_NAMES[word & 7]]
    elif word in {value: name for name, value in FIXED.items()}:
        mnemonic = {value: name for name, value in FIXED.items()}[word]
    elif word & 0o177400 in TRAPS.values():
        mnemonic = {value: name for name, value in TRAPS.items()}[word & 0o177400]
        operands = [f"{word & 0xFF:03o}"]
    else:
        single_base = word & 0o177700
        reverse_single = {value: name for name, value in SINGLE.items()}
        if single_base not in reverse_single:
            raise UnsupportedInstruction(f"unsupported instruction word {word:06o}")
        mnemonic = reverse_single[single_base]
        dst, index = _take_operand(word & 0o77, words, index, address + 2 * index)
        operands = [dst]
    return DecodedInstruction(address, mnemonic, tuple(operands), tuple(_word(w) for w in words[:index]))


def decode_stream(words: Sequence[int], start_address: int = 0) -> list[DecodedInstruction]:
    result: list[DecodedInstruction] = []
    index = 0
    while index < len(words):
        instruction = decode_one(words[index:], (start_address + 2 * index) & 0xFFFF)
        result.append(instruction)
        index += len(instruction.words)
    return result


def _octal(text: str) -> int:
    try:
        return int(text, 8)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"invalid octal value: {text}") from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    decode_parser = sub.add_parser("decode", help="decode an address-aware word stream")
    decode_parser.add_argument("words", nargs="+", type=_octal)
    decode_parser.add_argument("--address", type=_octal, default=0)
    byte_parser = sub.add_parser("bytes", help="show little-endian bytes for words")
    byte_parser.add_argument("words", nargs="+", type=_octal)
    branch_parser = sub.add_parser("branch", help="encode a branch target")
    branch_parser.add_argument("mnemonic", choices=sorted(BRANCH))
    branch_parser.add_argument("address", type=_octal)
    branch_parser.add_argument("target", type=_octal)
    args = parser.parse_args(argv)
    if args.command == "decode":
        for instruction in decode_stream(args.words, args.address):
            print(instruction)
    elif args.command == "bytes":
        print(" ".join(f"{byte:02x}" for byte in words_to_bytes(args.words)))
    else:
        print(f"{encode(args.mnemonic, address=args.address, target=args.target)[0]:06o}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
