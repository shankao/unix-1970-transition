#!/usr/bin/env python3
"""Run Stage-3B test L using only words emitted by PDP-7 as11.

This is class-M transport/validation instrumentation.  It parses native
``i``/``x``/``w`` records and deposits those exact values; it contains no
PDP-11 instruction encoder and never substitutes oracle-generated words.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import io
from pathlib import Path
import re
import subprocess
import tempfile

import pexpect

from build_stage3b import L, build_images
from pdp11_oracle import decode_one
from run_stage4a import BUILD, IMAGE, ROOT, Session, git_status, sha256
from run_stage4b import clean_cat


SOURCE = ROOT / "tests/pdp7-as11/stage3b-gold.s"
EVIDENCE = ROOT / "evidence/stage3-gold"
RECORD_RE = re.compile(r"^([ixw]) ([0-7]{6}) ([0-7]{6})$")
META_RE = re.compile(r"^(?:l [a-z_][a-z0-9_]{0,7}|n [0-9]) [0-7]{6}$")


@dataclass(frozen=True)
class TraceWord:
    kind: str
    address: int
    word: int


def parse_trace(text: str) -> tuple[TraceWord, ...]:
    """Parse native semantic records without interpreting assembly syntax."""
    result: list[TraceWord] = []
    occupied: set[int] = set()
    for number, line in enumerate(text.splitlines(), 1):
        if META_RE.fullmatch(line):
            continue
        match = RECORD_RE.fullmatch(line)
        if not match:
            raise ValueError(f"malformed native trace line {number}: {line!r}")
        kind, address_text, word_text = match.groups()
        address, word = int(address_text, 8), int(word_text, 8)
        if address & 1 or address >= 0o060000:
            raise ValueError(f"invalid PDP-11 address on trace line {number}")
        if address in occupied:
            raise ValueError(f"duplicate/conflicting address {address:06o}")
        occupied.add(address)
        result.append(TraceWord(kind, address, word))
    if not result:
        raise ValueError("native trace contains no machine words")
    return tuple(result)


def validate_stage3b_l(records: tuple[TraceWord, ...]) -> None:
    """Compare native output to independent Stage-3 source/oracle evidence."""
    expected = build_images()["l"].words
    actual_map = {item.address: item for item in records}
    expected_map = {item.address: item for item in expected}
    if set(actual_map) != set(expected_map):
        missing = sorted(set(expected_map) - set(actual_map))
        extra = sorted(set(actual_map) - set(expected_map))
        raise ValueError(f"native/Stage-3 layout differs: missing={missing} extra={extra}")
    kinds = {"instruction": "i", "extension": "x", "thread/data": "w"}
    for address, reference in expected_map.items():
        native = actual_map[address]
        if native.kind != kinds[reference.kind] or native.word != reference.word:
            raise ValueError(
                f"native word differs at {address:06o}: "
                f"{native.kind} {native.word:06o} != "
                f"{kinds[reference.kind]} {reference.word:06o}"
            )

    # Decode native instruction groups directly.  The oracle is a verifier;
    # these decoded values are never used to form the execution map.
    ordered = sorted(records, key=lambda item: item.address)
    by_address = {item.address: item for item in ordered}
    for item in ordered:
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


def simh_script(records: tuple[TraceWord, ...], log_path: Path) -> str:
    lines = [
        "; Stage-3 gold transport: every dep value came from PDP-7 as11.",
        f"set log -n {log_path}",
        "do machines/pdp11/late-summer-1970.simh",
    ]
    lines.extend(
        f"dep {item.address:06o} {item.word:06o}"
        for item in sorted(records, key=lambda item: item.address)
    )
    lines.extend((
        "echo STAGE3-GOLD START=001000 EXPECT=D",
        "go 001000",
        "echo",
        "echo STAGE3-GOLD HALTED",
        "examine pc,r2,r3,r4,r5",
        "examine 005000-005012",
        "show cpu",
        "show dev",
        "show ptr",
        "quit",
        "",
    ))
    return "\n".join(lines)


def assemble_source_on_pdp7(source: Path, native_stem: str,
                            evidence: Path, record: bool) -> tuple[str, str]:
    """Install and assemble one source using the resident native PDP-7 as11."""
    if not re.fullmatch(r"[a-z0-9]{1,6}", native_stem):
        raise ValueError("native stem must leave room for a PDP-7 .s/.o suffix")
    pre_status, pre_hash = git_status(), sha256(IMAGE)
    transcript = io.StringIO()
    child = pexpect.spawn(
        str(BUILD / "pdp7"), ["unixv0.simh"], cwd=str(BUILD),
        encoding="latin1", timeout=30,
    )
    child.logfile_read = transcript
    session = Session(child)
    try:
        child.expect_exact("login:")
        session.line("shankao")
        child.expect_exact("password:")
        session.line("shankao")
        child.expect_exact("@ ")
        native_source = native_stem + ".s"
        native_output = native_stem + ".o"
        session.command(f"rm {native_source}")
        session.install(native_source, source.read_text(encoding="ascii"))
        session.command(f"rm {native_output}")
        result = session.command(
            f"a.out {native_source} {native_output}", timeout=900
        )
        if "?" in result:
            raise RuntimeError("native as11 execution failed: " + repr(result))
        trace = clean_cat(session.command(f"cat {native_output}", timeout=300))
    finally:
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)
    state = (
        f"pre_sha256={pre_hash}\npost_sha256={sha256(IMAGE)}\n"
        "pre_git_status:\n" + pre_status + "post_git_status:\n" + git_status()
    )
    if record:
        evidence.mkdir(parents=True, exist_ok=True)
        (evidence / "pdp7-session.transcript.txt").write_text(
            transcript.getvalue(), encoding="latin1"
        )
        (evidence / "image-state.txt").write_text(state, encoding="utf-8")
    return trace, transcript.getvalue()


def assemble_on_pdp7(record: bool) -> tuple[str, str]:
    return assemble_source_on_pdp7(SOURCE, "gold", EVIDENCE, record)


def run(record: bool, reuse_trace: bool) -> None:
    if reuse_trace:
        trace = (EVIDENCE / "native-trace.txt").read_text(encoding="ascii")
    else:
        trace, _ = assemble_on_pdp7(record)
    records = parse_trace(trace)
    validate_stage3b_l(records)
    if record:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        trace_path = EVIDENCE / "native-trace.txt"
        script_path = EVIDENCE / "test-l.simh"
        log_path = EVIDENCE / "pdp11-session.transcript.txt"
        trace_path.write_text(trace, encoding="ascii")
        # SIMH command parsing does not quote the repository path's spaces;
        # run from ROOT and use this stable repository-relative log name.
        log_command_path = Path("evidence/stage3-gold/pdp11-session.transcript.txt")
        script_path.write_text(simh_script(records, log_command_path), encoding="ascii")
        temporary = None
    else:
        temporary = tempfile.TemporaryDirectory(prefix="stage3-gold-")
        directory = Path(temporary.name)
        script_path = directory / "test-l.simh"
        log_path = directory / "pdp11-session.transcript.txt"
        script_path.write_text(simh_script(records, log_path), encoding="ascii")
    completed = subprocess.run(
        ["pdp11", str(script_path)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
    )
    transcript = log_path.read_text(encoding="utf-8")
    if "STAGE3-GOLD START=001000 EXPECT=D\nD\nHALT instruction" not in transcript:
        raise RuntimeError("PDP-11 did not produce the Stage-3B test-L result D")
    if record:
        (EVIDENCE / "pdp11-stdout.txt").write_text(
            completed.stdout, encoding="utf-8"
        )
    if temporary is not None:
        temporary.cleanup()
    instructions = sum(item.kind == "i" for item in records)
    print(f"PASS words={len(records)} instructions={instructions} output=D")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--reuse-trace", action="store_true")
    args = parser.parse_args()
    run(args.record, args.reuse_trace)


if __name__ == "__main__":
    main()
