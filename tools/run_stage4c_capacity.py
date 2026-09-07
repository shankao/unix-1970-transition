#!/usr/bin/env python3
"""Characterize Stage 4C capacity on authoritative PDP-7 (class M)."""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path

import pexpect

from run_stage4a import ROOT, BUILD, IMAGE, Session, git_status, sha256
from run_stage4b import clean_cat


EVIDENCE = ROOT / "evidence/stage4c-capacity"
STAGE3 = ROOT / "tests/pdp7-as11/stage4c-stage3-shaped.s"


def oct6(value: int) -> str:
    return f"{value & 0o177777:06o}"


def capacity_source(globals_: int, locals_: int) -> tuple[str, str]:
    """Return a fixed stress source and its independently explicit trace."""
    assigned = min(16, globals_)
    lines = ["/ stage 4c capacity characterization", ".=002000"]
    trace = []
    for i in range(assigned):
        name = f"a{i:02o}"
        value = i
        lines.append(f"{name}={value:o}")
        trace.append(f"a {name} {oct6(value)}\n")
    address = 0o2000
    for i in range(globals_ - assigned):
        name = f"s{i:02o}"
        source = f"a{i % assigned:02o}" if assigned else "0"
        value = i % assigned if assigned else 0
        lines.append(f"{name}:;{source}")
        trace.append(f"l {name} {oct6(address)}\n")
        trace.append(f"w {oct6(address)} {oct6(value)}\n")
        address += 2
    for i in range(locals_):
        digit = i % 10
        lines.append(f"{digit}:;{digit}b")
        trace.append(f"n {digit} {oct6(address)}\n")
        trace.append(f"w {oct6(address)} {oct6(address)}\n")
        address += 2
    lines.append("/ padding makes every case cross the 128-character input refill boundary")
    return "\n".join(lines) + "\n", "".join(trace)


CASES = [
    (17, 5), (24, 5), (32, 5), (36, 5), (37, 5), (38, 5), (39, 5),
    (40, 5), (44, 5), (48, 5),
    (24, 0), (24, 10), (32, 10), (40, 10), (48, 10),
    (38, 10), (39, 0), (39, 10),
    (39, 2), (39, 4),
    (39, 1),
]


def run(record: bool, start: int, stop: int | None, stage3_only: bool) -> None:
    if record:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
    pre_hash = sha256(IMAGE)
    pre_status = git_status()
    transcript = io.StringIO()
    rows = []
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
        # Use the already-installed Stage 4C a.out. No source transfer/build.
        end = start if stage3_only else (len(CASES) if stop is None else min(stop, len(CASES)))
        for index in range(start, end):
            globals_, locals_ = CASES[index]
            source, expected = capacity_source(globals_, locals_)
            native = f"c{index:02o}.s"
            output = f"c{index:02o}.o"
            session.command(f"rm {native}")
            session.install(native, source)
            session.command(f"rm {output}")
            command_result = session.command(f"a.out {native} {output}", timeout=600)
            observed = clean_cat(session.command(f"cat {output}", timeout=180))
            success = observed == expected and "?" not in command_result
            arena_low = 0o17537 - (globals_ - 1) * 5 if globals_ else 0o17542
            # a.out is loaded at 010000 and its final bi.s word is stack at
            # 017157; count addresses available before the first global word.
            static_gap = arena_low - 0o17157
            rows.append((globals_, locals_, len(source), success, static_gap,
                         hashlib.sha256(observed.encode("ascii")).hexdigest()))
            if record:
                (EVIDENCE / f"g{globals_:02d}-l{locals_:02d}.s").write_text(
                    source, encoding="ascii")
                (EVIDENCE / f"g{globals_:02d}-l{locals_:02d}.out").write_text(
                    observed, encoding="ascii")

        if stage3_only:
            session.command("rm s3cap.s")
            session.install("s3cap.s", STAGE3.read_text(encoding="ascii"))
            session.command("rm s3cap.o")
            command_result = session.command("a.out s3cap.s s3cap.o", timeout=600)
            stage3_output = clean_cat(session.command("cat s3cap.o", timeout=180))
            if record:
                (EVIDENCE / "stage3-shaped.out").write_text(stage3_output, encoding="ascii")
            rows.append((17, 5, len(STAGE3.read_text(encoding="ascii")),
                         bool(stage3_output) and "?" not in command_result, 0,
                         hashlib.sha256(stage3_output.encode("ascii")).hexdigest()))
    finally:
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)

    post_hash = sha256(IMAGE)
    if record:
        matrix = ["kind\tglobals\tlocals\thost_bytes\tresult\tstatic_gap_words\toutput_sha256"]
        for index, row in enumerate(rows):
            kind = "matrix" if index < len(CASES) else "stage3-shaped"
            g, l, size, ok, gap, digest = row
            matrix.append(f"{kind}\t{g}\t{l}\t{size}\t{'PASS' if ok else 'FAIL'}\t{gap}\t{digest}")
        suffix = "stage3" if stage3_only else f"{start:02d}-{end:02d}"
        (EVIDENCE / f"capacity-{suffix}.tsv").write_text(
            "\n".join(matrix) + "\n")
        (EVIDENCE / f"session-{suffix}.transcript.txt").write_text(
            transcript.getvalue(), encoding="latin1")
        (EVIDENCE / f"image-{suffix}.txt").write_text(
            f"pre_sha256={pre_hash}\npost_sha256={post_hash}\n"
            f"pre_git_status:\n{pre_status}post_git_status:\n{git_status()}",
            encoding="utf-8")
    print(f"pre={pre_hash} post={post_hash}")
    for row in rows:
        print(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--stop", type=int)
    parser.add_argument("--stage3-only", action="store_true")
    args = parser.parse_args()
    run(args.record, args.start, args.stop, args.stage3_only)


if __name__ == "__main__":
    main()
