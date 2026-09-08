#!/usr/bin/env python3
"""Assemble and run the two-byte KL11 polling diagnostic (class M harness)."""

from __future__ import annotations

import argparse
import io
from pathlib import Path

import pexpect

from pdp11_oracle import decode_one
from run_stage3_gold import (
    ROOT, TraceWord, assemble_source_on_pdp7, parse_trace,
)


SOURCE = ROOT / "tests/pdp7-as11/kl11-poll.s"
ARTIFACT = ROOT / "artifacts/kl11-poll.simh"
EVIDENCE = ROOT / "evidence/kl11-poll"
ENTRY = 0o001000
FIRST = 0o001100
SECOND = 0o001102

EXPECTED = (
    ("TSTB", ("@#177560",)), ("BPL", ("001000",)),
    ("MOVB", ("@#177562", "R0")), ("MOVB", ("R0", "001100")),
    ("TSTB", ("@#177564",)), ("BPL", ("001016",)),
    ("MOVB", ("R0", "@#177566")),
    ("TSTB", ("@#177564",)), ("BPL", ("001030",)),
    ("TSTB", ("@#177560",)), ("BPL", ("001036",)),
    ("MOVB", ("@#177562", "R1")), ("MOVB", ("R1", "001102")),
    ("TSTB", ("@#177564",)), ("BPL", ("001054",)),
    ("MOVB", ("R1", "@#177566")),
    ("TSTB", ("@#177564",)), ("BPL", ("001066",)),
    ("HALT", ()),
)


def decoded_instructions(records: tuple[TraceWord, ...]):
    by_address = {item.address: item for item in records}
    result = []
    for item in sorted(records, key=lambda value: value.address):
        if item.kind != "i":
            continue
        words = [item.word]
        address = item.address + 2
        while address in by_address and by_address[address].kind == "x":
            words.append(by_address[address].word)
            address += 2
        decoded = decode_one(words, item.address)
        if tuple(words) != decoded.words:
            raise ValueError(f"oracle length mismatch at {item.address:06o}")
        result.append(decoded)
    return tuple(result)


def validate(records: tuple[TraceWord, ...]) -> None:
    decoded = decoded_instructions(records)
    observed = tuple((item.mnemonic, item.operands) for item in decoded)
    if observed != EXPECTED:
        raise ValueError(f"native instructions differ from fixture contract: {observed!r}")
    raw = {(item.address, item.word) for item in records if item.kind == "w"}
    if raw != {(FIRST, 0), (SECOND, 0)}:
        raise ValueError(f"unexpected scratch-data map: {sorted(raw)!r}")


def manual_script(records: tuple[TraceWord, ...]) -> str:
    lines = [
        "; Generated from native PDP-7 as11 output; no host-encoded words.",
        "; Type two characters after the READY message; each is echoed once.",
        "do machines/pdp11/late-summer-1970.simh",
    ]
    lines.extend(
        f"dep {item.address:06o} {item.word:06o}"
        for item in sorted(records, key=lambda value: value.address)
    )
    lines.extend((
        "echo KL11-POLL READY EXPECT=AB",
        f"go {ENTRY:06o}",
        "",
    ))
    return "\n".join(lines)


def execute_interactively(script: Path, record: bool) -> str:
    transcript = io.StringIO()
    child = pexpect.spawn(
        "pdp11", [str(script)], cwd=str(ROOT), encoding="latin1", timeout=20,
    )
    child.logfile_read = transcript
    try:
        child.expect_exact("KL11-POLL READY EXPECT=AB")
        child.setecho(False)
        child.send("A")
        child.expect_exact("A")
        child.send("B")
        child.expect_exact("B")
        child.expect_exact("HALT instruction")
        child.expect_exact("sim>")
        child.sendline(f"examine {FIRST:06o}-{SECOND:06o}")
        child.expect_exact("sim>")
        examine = child.before.replace("\r", "")
        if "1100:\t000101" not in examine or "1102:\t000102" not in examine:
            raise RuntimeError("saved KL11 input bytes do not equal A/B")
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)
    finally:
        if child.isalive():
            child.close(force=True)
    value = transcript.getvalue()
    if record:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        (EVIDENCE / "pdp11-session.transcript.txt").write_text(
            value, encoding="latin1"
        )
    return value


def run(record: bool, reuse_trace: bool) -> None:
    if reuse_trace:
        trace = (EVIDENCE / "native-trace.txt").read_text(encoding="ascii")
    else:
        trace, _ = assemble_source_on_pdp7(SOURCE, "klpoll", EVIDENCE, record)
    records = parse_trace(trace)
    if record:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        (EVIDENCE / "native-trace.txt").write_text(trace, encoding="ascii")
    validate(records)
    ARTIFACT.write_text(manual_script(records), encoding="ascii")
    execute_interactively(ARTIFACT, record)
    count = sum(item.kind == "i" for item in records)
    print(f"PASS words={len(records)} instructions={count} input=AB output=AB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--reuse-trace", action="store_true")
    args = parser.parse_args()
    run(args.record, args.reuse_trace)


if __name__ == "__main__":
    main()
