#!/usr/bin/env python3
"""Run the Stage 4A proof on the authoritative evolving PDP-7 host."""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import re
import subprocess
import time

import pexpect


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "machines/pdp7/pdp7-unix/build"
IMAGE = BUILD / "image-shankao.fs"
PDP7 = BUILD / "pdp7"
PDP7_CONFIG = ROOT / "machines/pdp7/pdp7.simh"
SOURCE_FILES = {
    "io.b": ROOT / "tests/pdp7-as11/io_probe.b",
    "rewind.s": ROOT / "src/pdp7/as11/rewind.s",
    "input": ROOT / "tests/pdp7-as11/input.txt",
}
RUNTIME_COPIES = {
    "s4bl.s": ROOT / "machines/pdp7/pdp7-unix/src/cmd/bl.s",
    "s4bi.s": ROOT / "machines/pdp7/pdp7-unix/src/cmd/bi.s",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_status() -> str:
    return subprocess.run(
        ["git", "status", "--short"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, check=True
    ).stdout


def expected_result(input_text: str) -> str:
    p17 = input_text[:17]
    p173 = input_text[:173]
    return (
        "a1\n" + p17 + "\na2\n" + p17 + "\n"
        + "b1\n" + p173 + "\nb2\n" + p173 + "\n"
        + f"ce\n000004\n{len(input_text):06o}\n"
        + "cr\n" + p17 + "\n"
        + "o:\n000000\n000001\n077777\n100000\n177777\n"
    )


class Session:
    def __init__(self, child: pexpect.spawn):
        self.child = child

    def line(self, value: str) -> None:
        # Send one native editor/shell line at a time and wait for its echoed
        # newline before proceeding.  Queuing multiple lines corrupted Stage 1
        # transfers; matching individual repeated characters can also run
        # ahead of PDP-7 consumption.
        for char in value + "\r":
            self.child.send(char)
            time.sleep(0.08)
        self.child.expect_exact("\n")

    def command(self, value: str, timeout: int = 120) -> str:
        self.line(value)
        self.child.expect_exact("@ ", timeout=timeout)
        return self.child.before

    def install(self, name: str, text: str) -> None:
        self.line("ed")
        self.child.expect_exact("edit")
        self.line("a")
        for line in text.splitlines():
            if "#" in line or "@" in line:
                raise ValueError(f"tty editing character in {name}: {line!r}")
            self.line(line)
        self.line(".")
        self.line(f"w {name}")
        self.child.expect(r"[0-9]+\r?\n", timeout=60)
        self.line("q")
        self.child.expect_exact("@ ", timeout=30)


def normalized_cat(raw: str) -> str:
    result = raw.replace("\r", "").replace("\x00", "")
    if result.startswith("\n"):
        result = result[1:]
    return result


def run(record: bool) -> None:
    pre_status = git_status()
    image_before = sha256(IMAGE)
    bl = ROOT / "machines/pdp7/pdp7-unix/src/cmd/bl.s"
    bl_before = sha256(bl)
    input_text = SOURCE_FILES["input"].read_text(encoding="ascii")
    expected = expected_result(input_text)
    transcript = io.StringIO()

    child = pexpect.spawn(
        str(PDP7), [str(PDP7_CONFIG)], cwd=str(ROOT),
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

        # These names are Stage-4A-owned working/build artifacts.  Removing
        # them makes a rerun deterministic without touching shared originals.
        for name in ("io.b", "io.s", "rewind.s", "input", "result", "a.out"):
            session.command(f"rm {name}")
        # PDP-7 UNIX does not accept a modern compound pathname here.  The
        # live discovery session established that `ch dd dmr` can traverse to
        # the originals, but ordinary commands then fail under dmr ownership.
        # Copy the already-present shankao op.s natively and transfer exact
        # checked-in bl.s/bi.s text into shankao-owned working files.
        output = session.command("stat s4op.s")
        if "?" in output:
            output = session.command("cp op.s s4op.s")
            if "?" in output:
                raise RuntimeError("working copy failed: op.s -> s4op.s")
        for name, path in RUNTIME_COPIES.items():
            output = session.command(f"stat {name}")
            expected_words = (path.stat().st_size + 1) // 2
            if "?" in output or f"{expected_words:05o}" not in output:
                session.command(f"rm {name}")
                session.install(name, path.read_text(encoding="ascii"))

        for name, path in SOURCE_FILES.items():
            session.install(name, path.read_text(encoding="ascii"))

        compile_output = session.command("b io.b io.s", timeout=300)
        if "?" in compile_output:
            raise RuntimeError("B compilation failed")
        assemble_output = session.command(
            "as s4op.s s4bl.s io.s rewind.s s4bi.s", timeout=300
        )
        if ("?" in assemble_output or "I" not in assemble_output
                or "II" not in assemble_output
                or re.search(r"(?:^|[\r\n])[a-z] [0-9]{4}(?:[\r\n]|$)", assemble_output)):
            raise RuntimeError("assembly/link failed")
        execute_output = session.command("a.out input result", timeout=300)
        if "?" in execute_output:
            raise RuntimeError("probe execution failed")
        observed = normalized_cat(session.command("cat result", timeout=120))
        if observed != expected:
            raise AssertionError(
                f"PDP-7 result differs: expected {len(expected)} chars, "
                f"observed {len(observed)} chars"
            )
    finally:
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)

    image_after = sha256(IMAGE)
    if sha256(bl) != bl_before:
        raise AssertionError("authentic bl.s changed")

    post_status = git_status()

    if record:
        evidence = ROOT / "evidence/stage4a"
        (evidence / "result.txt").write_text(observed, encoding="ascii")
        (evidence / "session.transcript.txt").write_text(
            transcript.getvalue(), encoding="latin1"
        )
        (evidence / "image-state.txt").write_text(
            "image=machines/pdp7/pdp7-unix/build/image-shankao.fs\n"
            f"pre_sha256={image_before}\npost_sha256={image_after}\n"
            "pre_git_status:\n" + pre_status
            + "post_git_status:\n" + post_status,
            encoding="utf-8",
        )
    print(
        f"PASS input={len(input_text)} pre_sha256={image_before} "
        f"post_sha256={image_after}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    run(args.record)


if __name__ == "__main__":
    main()
