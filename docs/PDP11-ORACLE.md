# PDP-11/20 verification oracle

`tools/pdp11_oracle.py` is class **M** modern instrumentation. It independently
checks words produced by later reconstruction stages; it is not an assembler,
emulator, historical artifact, or dependency of the final PDP-7-to-paper-tape
workflow.

## Historical boundary

The encoded target is the base KA11/PDP-11/20 repertoire described by DEC's
*PDP-11 Handbook*, Second Edition (1970). KE11-A was a separately priced
arithmetic peripheral, not the later EIS instruction set. This project keeps
KE11 disabled and the oracle explicitly rejects `MUL`, `DIV`, `ASH`, `ASHC`,
`SOB`, and `XOR`.

Program-visible addresses are 16-bit software addresses. In particular:

| Device register | Address |
| --- | ---: |
| KL11 TKS | `177560` |
| KL11 TKB | `177562` |
| KL11 TPS | `177564` |
| KL11 TPB | `177566` |
| PC11 PRS | `177550` |
| PC11 PRB | `177552` |

KL11 keyboard/reader and teleprinter/punch vectors are `060` and `064`; the
PC11 reader vector is `070`. Do not substitute SIMH's extended
UNIBUS/physical-address display notation in generated PDP-11 code.

## Interface and supported instructions

The Python API provides `Operand`, `encode_specifier`, `decode_specifier`,
`encode`, `decode_one`, `decode_stream`, `branch_displacement`,
`branch_target`, and `words_to_bytes`. Numeric display is octal. The small CLI
provides address-aware `decode`, little-endian `bytes`, and `branch` commands:

```sh
python3 tools/pdp11_oracle.py decode --address 057744 016701 000026
python3 tools/pdp11_oracle.py bytes 012700 177566
python3 tools/pdp11_oracle.py branch BR 001000 001010
```

The table-driven encoder/decoder supports:

- double operand: `MOV/MOVB`, `CMP/CMPB`, `BIT/BITB`, `BIC/BICB`,
  `BIS/BISB`, `ADD`, `SUB`;
- branches: `BR`, `BNE`, `BEQ`, `BGE`, `BLT`, `BGT`, `BLE`, `BPL`, `BMI`,
  `BHI`, `BLOS`, `BVC`, `BVS`, `BCC/BHIS`, `BCS/BLO`;
- control: `JMP`, `JSR`, `RTS`;
- single operand: `CLR/CLRB`, `COM/COMB`, `INC/INCB`, `DEC/DECB`,
  `NEG/NEGB`, `ADC/ADCB`, `SBC/SBCB`, `TST/TSTB`, `ROR/RORB`, `ROL/ROLB`,
  `ASR/ASRB`, `ASL/ASLB`, `SWAB`;
- condition/operate: `CLC`, `SEC`, `HALT`; and, at negligible table cost,
  `WAIT`, `RTI`, `IOT`, `RESET`, `EMT`, and `TRAP`.

All eight operand modes use `specifier = (mode << 3) | register`: register,
register deferred, autoincrement, autoincrement deferred, autodecrement,
autodecrement deferred, indexed, and indexed deferred. For PC/R7, modes 2, 3,
6, and 7 are immediate, absolute, relative, and relative deferred. Required
extension words are emitted in operand order. PC-relative display resolves the
target using the PC after fetching that operand's extension word.

Branches contain a signed eight-bit word displacement:

```text
encoded = (target - (instruction_address + 2)) / 2
target  = instruction_address + 2 + 2 * sign_extend_8(encoded)
```

Odd displacements and values outside `[-128,+127]` words are rejected.
`words_to_bytes` serializes each 16-bit word low byte first.

## Regression boundary and limitations

`tests/test_pdp11_oracle.py` stores independently supplied expected words as
literals, including DEC's printed `CMPB @#177560,#301` three-word example.
It also walks the documented bootstrap from `057744`, consuming extension
words and stopping before the final `177550` data word.

This is deliberately not a parser, symbol-table assembler, emulator, loader,
paper-tape formatter, or exhaustive PDP-11 disassembler. Stream decoding
requires the caller to identify code boundaries; arbitrary data can resemble
an instruction. PC-relative operands are accepted as encoded displacement
words and decoded to absolute targets; symbol resolution remains a later
tool's responsibility.

## Stage 3 coverage

| Stage 1/3 need | Oracle coverage or consequence |
| --- | --- |
| constants, load, store | `MOV` and all addressing modes |
| stack operations | autoincrement and autodecrement modes |
| addition, subtraction | `ADD`, `SUB` |
| comparisons, conditions | `CMP`, `TST`, and conditional branches |
| vectors, indirection | deferred and indexed modes |
| subroutine calls | `JSR`, `RTS` |
| threaded dispatch candidate | `JMP @(R3)+` |
| console character output | poll TPS `177564`; write TPB `177566` |
| multiplication/division/remainder | software implementation required |
| multi-bit shifts | loops using one-bit shifts/rotates |

Stage 3 used this oracle to verify hand-constructed runtime words and diagnose
extensions/branches. Later reconstructed tools should continue to use it as an
independent check. Class-B target code must not import or call this class-M
module, and no stage may silently acquire EIS or KE11 arithmetic.
