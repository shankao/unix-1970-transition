# SPDX-License-Identifier: GPL-3.0-only
"""Prove PDP-7 punch -> PDP-11 reader/DEC-loader transport for U1.

The acceptance tape is emitted by a native PDP-7 B program.  Python parses
and verifies it but never constructs or repairs its target records.
"""

from __future__ import annotations

import argparse
import io
from pathlib import Path
import re
import tempfile

import pexpect

from dec_abs import loader_bytes, parse_absolute, words_from_bytes
from run_stage3_gold import ROOT, TraceWord, parse_trace
from run_stage4a import IMAGE, PDP7, PDP7_CONFIG, Session, git_status, sha256
from run_stage4b import assembler_failed, clean_cat
from run_u1_substrate import (
    EVIDENCE as U1_EVIDENCE, labels_from_trace, validate_interrupt, validate_ram,
)


PUNCH_SOURCE = ROOT / "src/pdp7/abspunch/abspunch.b"
PUNCH_ADAPTER = ROOT / "src/pdp7/abspunch/punch.s"
LOADER_JSON = ROOT / "evidence/b4/DEC-11-L2PC-PO.json"
EVIDENCE = ROOT / "evidence/b4"
INT_TAPE = ROOT / "artifacts/u1-interrupt.ptap"
RAM_TAPE = ROOT / "artifacts/u1-ram.ptap"
BOOTSTRAP = (
    0o016701, 0o000026, 0o012702, 0o000352, 0o005211, 0o105711,
    0o100376, 0o116162, 0o000002, 0o057400, 0o005267, 0o177756,
    0o000765, 0o177550,
)
BOOT_BASE = 0o057744
ENTRY = 0o001000


def _attach_punch(child: pexpect.spawn, path: Path) -> None:
    child.sendcontrol("e"); child.expect_exact("sim>")
    child.sendline(f"attach ptp {path}"); child.expect_exact("sim>")
    child.sendline("continue")


def _detach_punch(child: pexpect.spawn) -> None:
    child.sendcontrol("e"); child.expect_exact("sim>")
    child.sendline("detach ptp"); child.expect_exact("sim>")
    child.sendline("continue")


def produce_on_pdp7(record: bool) -> tuple[dict[str, tuple[TraceWord, ...]], str]:
    """Verify the accepted U1 articles, then punch them inside PDP-7 UNIX."""
    pre_hash, pre_status = sha256(IMAGE), git_status()
    transcript = io.StringIO()
    traces: dict[str, tuple[TraceWord, ...]] = {}
    with tempfile.TemporaryDirectory(prefix="b4-punch-") as directory:
        temp = Path(directory)
        child = pexpect.spawn(str(PDP7), [str(PDP7_CONFIG)], cwd=str(ROOT),
                              encoding="latin1", timeout=30)
        child.logfile_read = transcript; session = Session(child)
        try:
            child.expect_exact("login:"); session.line("shankao")
            child.expect_exact("password:"); session.line("shankao")
            child.expect_exact("@ ")
            # U1's accepted native traces and resident .o files are the frozen
            # acceptance articles.  Do not retransmit or regenerate a subtly
            # different payload as part of transport acceptance.
            for stem, trace_name in (("u1int", "interrupt-native-trace.txt"),
                                     ("u1ram", "ram-native-trace.txt")):
                trace = (U1_EVIDENCE / trace_name).read_text(encoding="ascii")
                resident = clean_cat(session.command(f"cat {stem}.o", timeout=300))
                if resident != trace:
                    raise RuntimeError(f"resident native {stem}.o differs from U1 evidence")
                traces[stem] = parse_trace(trace)
                (EVIDENCE / f"{stem}-native-trace.txt").write_text(
                    trace, encoding="ascii")

            session.command("rm abspun.b"); session.install(
                "abspun.b", PUNCH_SOURCE.read_text(encoding="ascii"))
            session.command("rm punch.s"); session.install(
                "punch.s", PUNCH_ADAPTER.read_text(encoding="ascii"))
            session.command("rm abspun.s"); session.command("rm a.out")
            compiled = session.command("b abspun.b abspun.s", timeout=900)
            if "?" in compiled:
                raise RuntimeError("native B compilation of abspunch failed")
            linked = session.command(
                "as s4op.s s4bl.s abspun.s punch.s s4bi.s", timeout=900)
            if assembler_failed(linked):
                raise RuntimeError("native assembly/link of abspunch failed")

        finally:
            child.sendcontrol("e"); child.expect_exact("sim>", timeout=10)
            child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)

        # The punch special inode belongs to dd/system.  Use the restored
        # super-user account only for this device operation; inputs and the
        # executable cross the directory boundary through native `ln` links.
        child = pexpect.spawn(str(PDP7), [str(PDP7_CONFIG)], cwd=str(ROOT),
                              encoding="latin1", timeout=30)
        child.logfile_read = transcript; session = Session(child)
        try:
            child.expect_exact("login:"); session.line("system")
            child.expect_exact("password:"); session.line("system")
            child.expect_exact("@ ")
            for name in ("u1int.o", "u1ram.o", "a.out"):
                session.command(f"rm {name}")
                if "?" in session.command(f"ln shankao {name}"):
                    raise RuntimeError(f"system could not link shankao/{name}")
            for stem, destination in (("u1int", INT_TAPE), ("u1ram", RAM_TAPE)):
                punched = temp / f"{stem}.ptap"
                _attach_punch(child, punched)
                result = session.command(f"a.out {stem}.o b4sink", timeout=900)
                _detach_punch(child)
                if "?" in result:
                    raise RuntimeError(f"native punch failed for {stem}")
                destination.write_bytes(punched.read_bytes())
            session.command("rm u1int.o u1ram.o a.out b4sink")
        finally:
            child.sendcontrol("e"); child.expect_exact("sim>", timeout=10)
            child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)
    state = (f"pre_sha256={pre_hash}\npost_sha256={sha256(IMAGE)}\n"
             "pre_git_status:\n" + pre_status + "post_git_status:\n" + git_status())
    if record:
        (EVIDENCE / "pdp7-punch.transcript.txt").write_text(
            transcript.getvalue(), encoding="latin1")
        (EVIDENCE / "pdp7-image-state.txt").write_text(state, encoding="utf-8")
    return traces, transcript.getvalue()


def verify_tape(path: Path, records: tuple[TraceWord, ...]) -> tuple[int, int]:
    memory, transfer, record_count = parse_absolute(path.read_bytes())
    actual = words_from_bytes(memory)
    expected = {item.address: item.word for item in records}
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        wrong = sorted(a for a in set(actual) & set(expected)
                       if actual[a] != expected[a])
        raise ValueError(f"punched/native mismatch missing={missing} extra={extra} wrong={wrong}")
    if transfer != 1:
        raise ValueError(f"acceptance tape transfer address is {transfer!r}, not halt 1")
    return record_count, len(memory)


def _command(child: pexpect.spawn, command: str) -> str:
    child.sendline(command); child.expect_exact("sim>")
    return child.before.replace("\r", "")


def _examine(child: pexpect.spawn, address: int) -> int:
    text = _command(child, f"examine {address:06o}")
    match = re.search(rf"{address:o}:\s+([0-7]{{6}})", text)
    if not match:
        raise RuntimeError(f"cannot parse memory at {address:06o}: {text!r}")
    return int(match.group(1), 8)


def load_through_ptr(child: pexpect.spawn, loader: Path, payload: Path,
                     records: tuple[TraceWord, ...]) -> None:
    _command(child, "do machines/pdp11/pdp11.simh")
    _command(child, "set ptr enabled")
    _command(child, f"attach ptr {loader}")
    for offset, word in enumerate(BOOTSTRAP):
        _command(child, f"deposit {BOOT_BASE + 2*offset:06o} {word:06o}")
    child.sendline(f"go {BOOT_BASE:06o}")
    child.expect_exact("HALT instruction", timeout=20); child.expect_exact("sim>")
    _command(child, "detach ptr"); _command(child, f"attach ptr {payload}")
    child.sendline("go 057500")
    child.expect_exact("HALT instruction", timeout=30); child.expect_exact("sim>")
    for item in records:
        observed = _examine(child, item.address)
        if observed != item.word:
            raise RuntimeError(
                f"reader/loader identity failure at {item.address:06o}: "
                f"{observed:06o} != {item.word:06o}")


def replay_interrupt(child: pexpect.spawn, labels: dict[str, int]) -> None:
    child.sendline(f"go {ENTRY:06o}"); child.setecho(False)
    child.send("A"); child.expect_exact("A", timeout=20)
    child.send("B"); child.expect_exact("B", timeout=20)
    child.expect_exact("HALT instruction", timeout=20); child.expect_exact("sim>")
    expected = {"first":0o101,"second":0o102,"rxints":2,"txints":4,
                "txcount":2,"txchar":7,"trapres":0o12354,"savedps":4,
                "success":1}
    for name, value in expected.items():
        if _examine(child, labels[name]) != value:
            raise RuntimeError(f"interrupt replay failed at {name}")


def replay_ram(child: pexpect.spawn, labels: dict[str, int]) -> None:
    child.sendline(f"go {ENTRY:06o}")
    child.expect_exact("HALT instruction", timeout=20); child.expect_exact("sim>")
    for name, value in {"exhaust":0o177777,"procblk":2,
                        "freemap":0,"success":1}.items():
        if _examine(child, labels[name]) != value:
            raise RuntimeError(f"RAM replay failed at {name}")
    if _examine(child, 0o043000) != 0o65432:
        raise RuntimeError("RAM replay crossed its block boundary")


def historical_replay(records: dict[str, tuple[TraceWord, ...]], record: bool) -> str:
    loader_data = loader_bytes(LOADER_JSON)
    transcript = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="b4-loader-") as directory:
        loader = Path(directory) / "DEC-11-L2PC-PO.ptap"
        loader.write_bytes(loader_data)
        for stem, tape, replay in (
            ("u1int", INT_TAPE, replay_interrupt),
            ("u1ram", RAM_TAPE, replay_ram),
        ):
            child = pexpect.spawn("pdp11", cwd=str(ROOT), encoding="latin1", timeout=30)
            child.logfile_read = transcript
            try:
                load_through_ptr(child, loader, tape, records[stem])
                replay(child, labels_from_trace(
                    (EVIDENCE / f"{stem}-native-trace.txt").read_text(encoding="ascii")))
                child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)
            finally:
                if child.isalive(): child.close(force=True)
    value = transcript.getvalue().replace("\r", "")
    if record:
        (EVIDENCE / "pdp11-loader-replay.transcript.txt").write_text(
            value, encoding="latin1")
    return value


def run(record: bool) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    traces, _ = produce_on_pdp7(record)
    validate_interrupt(traces["u1int"], labels_from_trace(
        (EVIDENCE / "u1int-native-trace.txt").read_text(encoding="ascii")))
    validate_ram(traces["u1ram"])
    counts = {}
    for stem, tape in (("u1int", INT_TAPE), ("u1ram", RAM_TAPE)):
        counts[stem] = verify_tape(tape, traces[stem])
    historical_replay(traces, record)
    print("PASS B4.1=PASS B4.2=PASS B4.3=PASS B4.4=PASS U1.7=PASS "
          f"interrupt_records={counts['u1int'][0]} ram_records={counts['u1ram'][0]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    run(args.record)


if __name__ == "__main__":
    main()
