# SPDX-License-Identifier: GPL-3.0-only
"""Punch an era user's native as11 output and prepare its PDP-11 replay.

This is class-M operator automation, not a recovered PDP-7 command. The target
records are produced by the already-installed native PDP-7 formatter through
PTP; Python only captures and checks them and writes an operator command file.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import tempfile

import pexpect

from dec_abs import loader_bytes, parse_absolute, words_from_bytes
from run_b4_transport import BOOT_BASE, BOOTSTRAP, LOADER_JSON, _attach_punch, _detach_punch
from run_stage3_gold import ROOT, parse_trace
from run_stage4a import PDP7, Session
from run_stage4b import clean_cat


ERA = ROOT / "eras/pdp7-crossdev"
OUTPUT = ROOT / "artifacts/visitor"


def checked_name(value: str) -> str:
    """Accept one safe PDP-7 filename of at most eight characters."""
    if not re.fullmatch(r"[a-z][a-z0-9]{0,5}\.o", value):
        raise ValueError("use a lowercase .o name of at most eight characters, e.g. try.o")
    return value


def checked_records(text: str, entry: int):
    records = parse_trace(text)
    addresses = {item.address for item in records}
    if any(address >= 0o057400 for address in addresses):
        raise ValueError("payload overlaps the DEC loader/bootstrap area")
    if entry & 1 or entry not in addresses:
        raise ValueError("entry must be an even address present in the native trace")
    return records


def session(account: str) -> tuple[pexpect.spawn, Session]:
    child = pexpect.spawn(
        str(PDP7), ["pdp7.simh"], cwd=str(ERA), encoding="latin1", timeout=60
    )
    native = Session(child)
    child.expect_exact("login:"); native.line(account)
    child.expect_exact("password:"); native.line(account)
    child.expect_exact("@ ")
    return child, native


def close(child: pexpect.spawn) -> None:
    if child.isalive():
        child.sendcontrol("e"); child.expect_exact("sim>", timeout=10)
        child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)


def capture_trace(name: str, entry: int):
    child, native = session("shankao")
    try:
        text = clean_cat(native.command(f"cat {name}", timeout=300))
        return text, checked_records(text, entry)
    finally:
        close(child)


def native_punch(name: str, destination: Path) -> bytes:
    """Run the installed PDP-7 formatter as the authentic PTP owner."""
    linked: list[str] = []
    child, native = session("system")
    try:
        if "?" not in native.command("stat vout"):
            raise RuntimeError("system/vout already exists; refusing to replace it")
        for item in (name, "abspun"):
            if "?" not in native.command(f"stat {item}"):
                raise RuntimeError(f"system/{item} already exists; refusing to replace it")
            if "?" in native.command(f"ln shankao {item}"):
                raise RuntimeError(f"cannot link shankao/{item} into system")
            linked.append(item)
        with tempfile.TemporaryDirectory(prefix="pdp7-punch-") as directory:
            punched = Path(directory) / "visitor.ptap"
            _attach_punch(child, punched)
            result = native.command(f"abspun {name} vout", timeout=900)
            _detach_punch(child)
            if "?" in result:
                raise RuntimeError("native formatter reported an error")
            data = punched.read_bytes()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return data
    finally:
        for item in reversed(linked):
            native.command(f"rm {item}")
        native.command("rm vout")
        close(child)


def replay_text(stem: str, entry: int) -> str:
    lines = [
        "; Class-M operator replay using a contemporary class-C DEC loader.",
        "; Bell Labs' exact receiving loader and tape format remain unknown.",
        "; Only the historically plausible front-panel bootstrap is deposited.",
        "do machines/pdp11/pdp11.simh",
        "set ptr enabled",
        "attach ptr artifacts/visitor/dec-loader.ptap",
    ]
    lines.extend(
        f"deposit {BOOT_BASE + 2 * index:06o} {word:06o}"
        for index, word in enumerate(BOOTSTRAP)
    )
    lines.extend([
        f"go {BOOT_BASE:06o}",
        "detach ptr",
        f"attach ptr artifacts/visitor/{stem}.ptap",
        "go 057500",
        f"echo PDP-7-PUNCHED PROGRAM LOADED - STARTING AT {entry:06o}",
        f"go {entry:06o}",
        "examine r0",
    ])
    return "\n".join(lines) + "\n"


def export(name: str, entry: int = 0o1000) -> Path:
    name = checked_name(name)
    stem = name[:-2]
    print("Quit the PDP-7 first; reading your saved cross-development era disk.")
    trace, records = capture_trace(name, entry)
    tape_path = OUTPUT / f"{stem}.ptap"
    data = native_punch(name, tape_path)
    memory, transfer, count = parse_absolute(data)
    expected = {item.address: item.word for item in records}
    if words_from_bytes(memory) != expected or transfer != 1:
        tape_path.unlink(missing_ok=True)
        raise RuntimeError("punched tape does not exactly match native as11 output")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / f"{stem}.trace").write_text(trace, encoding="ascii")
    (OUTPUT / "dec-loader.ptap").write_bytes(loader_bytes(LOADER_JSON))
    replay = OUTPUT / f"{stem}.simh"
    replay.write_text(replay_text(stem, entry), encoding="ascii")
    print(f"Verified {len(records)} native words in {count} DEC records ({len(data)} bytes).")
    print(f"Carry the tape across with: pdp11 {replay.relative_to(ROOT)}")
    return replay


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="native as11 .o file in shankao's era directory")
    parser.add_argument("--entry", default="1000", help="entry address in octal (default: 1000)")
    args = parser.parse_args()
    try:
        export(args.name, int(args.entry, 8))
    except (ValueError, RuntimeError, OSError, pexpect.ExceptionPexpect) as error:
        sys.exit(f"punch failed: {error}")


if __name__ == "__main__":
    main()
