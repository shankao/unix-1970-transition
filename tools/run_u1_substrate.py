#!/usr/bin/env python3
"""Assemble and run the remaining bare-KA11 U1 substrate diagnostics.

This class-M harness transports native PDP-7 ``as11`` records unchanged.
It decodes instructions only to verify them and contains no PDP-11 encoder.
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path
import re

import pexpect

from run_kl11_poll import decoded_instructions
from run_stage3_gold import ROOT, TraceWord, assemble_source_on_pdp7, parse_trace


INT_SOURCE = ROOT / "tests/pdp7-as11/u1-interrupt.s"
RAM_SOURCE = ROOT / "tests/pdp7-as11/u1-ram.s"
INT_ARTIFACT = ROOT / "artifacts/u1-interrupt.simh"
RAM_ARTIFACT = ROOT / "artifacts/u1-ram.simh"
EVIDENCE = ROOT / "evidence/u1-substrate"
ENTRY = 0o001000
LABEL_RE = re.compile(r"^l ([a-z_][a-z0-9_]{0,7}) ([0-7]{6})$")


def labels_from_trace(trace: str) -> dict[str, int]:
    labels: dict[str, int] = {}
    for line in trace.splitlines():
        match = LABEL_RE.fullmatch(line)
        if match:
            name, address = match.groups()
            if name in labels:
                raise ValueError(f"duplicate native label {name}")
            labels[name] = int(address, 8)
    return labels


def validate_interrupt(records: tuple[TraceWord, ...], labels: dict[str, int]) -> None:
    decoded = decoded_instructions(records)
    mnemonics = [item.mnemonic for item in decoded]
    required = {"RTI", "TRAP", "BIC"}
    if missing := required - set(mnemonics):
        raise ValueError(f"interrupt fixture lacks instructions: {sorted(missing)}")
    if mnemonics.count("RTI") != 3 or mnemonics.count("TRAP") != 1:
        raise ValueError("fixture must contain three RTIs and one diagnostic TRAP")
    words = {item.address: item.word for item in records}
    vectors = {
        0o34: labels["trapent"], 0o36: 0,
        0o60: labels["rxint"], 0o62: 0o200,
        0o64: labels["txint"], 0o66: 0o200,
    }
    for address, expected in vectors.items():
        if words.get(address) != expected:
            raise ValueError(f"bad native vector at {address:06o}")
    source = INT_SOURCE.read_text(encoding="ascii")
    if "tstb *$177560" in source or "tstb *$177564" in source:
        raise ValueError("interrupt fixture contains a KL11 polling loop")


def validate_ram(records: tuple[TraceWord, ...]) -> None:
    mnemonics = {item.mnemonic for item in decoded_instructions(records)}
    if missing := {"BIT", "BIC", "BIS"} - mnemonics:
        raise ValueError(f"RAM fixture lacks instructions: {sorted(missing)}")


def simh_script(records: tuple[TraceWord, ...], title: str) -> str:
    lines = [
        "; Exact deposits emitted by native PDP-7 as11; host does not encode.",
        "do machines/pdp11/pdp11.simh",
    ]
    lines.extend(f"dep {item.address:06o} {item.word:06o}"
                 for item in sorted(records, key=lambda value: value.address))
    lines.extend((f"echo {title}", f"go {ENTRY:06o}", ""))
    return "\n".join(lines)


def _examine(child: pexpect.spawn, address: int) -> int:
    child.sendline(f"examine {address:06o}")
    child.expect_exact("sim>")
    text = child.before.replace("\r", "")
    match = re.search(rf"{address:o}:\s+([0-7]{{6}})", text)
    if not match:
        raise RuntimeError(f"could not parse examine {address:06o}: {text!r}")
    return int(match.group(1), 8)


def execute_interrupt(script: Path, labels: dict[str, int], record: bool) -> str:
    transcript = io.StringIO()
    child = pexpect.spawn("pdp11", [str(script)], cwd=str(ROOT),
                          encoding="latin1", timeout=20)
    child.logfile_read = transcript
    try:
        child.expect_exact("U1 INTERRUPT READY - TYPE 2 CHARACTERS")
        child.setecho(False)
        child.send("A"); child.expect_exact("A")
        child.send("B"); child.expect_exact("B")
        child.expect_exact("HALT instruction"); child.expect_exact("sim>")
        expected = {
            "first": 0o101, "second": 0o102, "rxints": 2,
            "txints": 4, "txcount": 2, "txchar": 7,
            "trapres": 0o12354, "savedps": 0o4, "success": 1,
        }
        for name, value in expected.items():
            observed = _examine(child, labels[name])
            if observed != value:
                raise RuntimeError(f"{name}={observed:06o}, expected {value:06o}")
        saved_pc = _examine(child, labels["savedpc"])
        if saved_pc not in (0o001012, 0o001016):
            raise RuntimeError(f"interrupt frame has unexpected PC {saved_pc:06o}")
        child.sendline("examine sp"); child.expect_exact("sim>")
        if "SP:\t027000" not in child.before.replace("\r", ""):
            raise RuntimeError("RTI/TRAP frames did not restore the initial stack")
        child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)
    finally:
        if child.isalive(): child.close(force=True)
    value = transcript.getvalue().replace("\r", "")
    if record:
        (EVIDENCE / "interrupt-pdp11.transcript.txt").write_text(
            value, encoding="latin1")
    return value


def execute_ram(script: Path, labels: dict[str, int], record: bool) -> str:
    transcript = io.StringIO()
    child = pexpect.spawn("pdp11", [str(script)], cwd=str(ROOT),
                          encoding="latin1", timeout=20)
    child.logfile_read = transcript
    try:
        child.expect_exact("U1 RAM STORAGE START")
        child.expect_exact("HALT instruction"); child.expect_exact("sim>")
        expected = {"exhaust": 0o177777, "procblk": 2,
                    "freemap": 0, "success": 1}
        failures = []
        for name, value in expected.items():
            observed = _examine(child, labels[name])
            if observed != value:
                failures.append(f"{name}={observed:06o}, expected {value:06o}")
        if _examine(child, 0o043000) != 0o65432:
            failures.append("512-byte copy crossed into the next RAM block")
        for index in (0, 1, 0o377):
            if _examine(child, 0o042000 + index * 2) != index:
                failures.append("RAM block write/read round trip failed")
                break
        allocated = [_examine(child, labels["allocs"] + 2*i) for i in range(14)]
        if allocated != list(range(2, 0o20)):
            failures.append(f"block reservation/order failure: {allocated!r}")
        if failures:
            raise RuntimeError("; ".join(failures))
        child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)
    finally:
        if child.isalive(): child.close(force=True)
    value = transcript.getvalue().replace("\r", "")
    if record:
        (EVIDENCE / "ram-pdp11.transcript.txt").write_text(
            value, encoding="latin1")
    return value


def _native(source: Path, stem: str, trace_name: str, record: bool,
            reuse: bool) -> tuple[tuple[TraceWord, ...], dict[str, int]]:
    path = EVIDENCE / trace_name
    if reuse:
        trace = path.read_text(encoding="ascii")
    else:
        trace, _ = assemble_source_on_pdp7(source, stem, EVIDENCE, record)
    if record: path.write_text(trace, encoding="ascii")
    return parse_trace(trace), labels_from_trace(trace)


def run(record: bool, reuse_interrupt: bool, reuse_ram: bool) -> None:
    if record: EVIDENCE.mkdir(parents=True, exist_ok=True)
    int_records, int_labels = _native(
        INT_SOURCE, "u1int", "interrupt-native-trace.txt", record, reuse_interrupt)
    validate_interrupt(int_records, int_labels)
    INT_ARTIFACT.write_text(simh_script(
        int_records, "U1 INTERRUPT READY - TYPE 2 CHARACTERS"), encoding="ascii")
    execute_interrupt(INT_ARTIFACT, int_labels, record)

    ram_records, ram_labels = _native(
        RAM_SOURCE, "u1ram", "ram-native-trace.txt", record, reuse_ram)
    validate_ram(ram_records)
    RAM_ARTIFACT.write_text(simh_script(
        ram_records, "U1 RAM STORAGE START"), encoding="ascii")
    execute_ram(RAM_ARTIFACT, ram_labels, record)
    instructions = sum(item.kind == "i" for item in int_records + ram_records)
    print(f"PASS words={len(int_records)+len(ram_records)} "
          f"instructions={instructions} U1.3=PASS U1.4=PASS U1.5=PASS U1.6=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--reuse-interrupt", action="store_true")
    parser.add_argument("--reuse-ram", action="store_true")
    args = parser.parse_args()
    run(args.record, args.reuse_interrupt, args.reuse_ram)


if __name__ == "__main__": main()
