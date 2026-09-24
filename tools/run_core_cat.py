# SPDX-License-Identifier: GPL-3.0-only
"""Build and run the first PDP-11 Unix cat command.

The PDP-7-hosted as11 produces every system and command word.  Python checks
and operates the machines; it never encodes or replaces PDP-11 instructions.
"""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import re
import shutil
import tempfile

import pexpect

from dec_abs import loader_bytes, parse_absolute, words_from_bytes
from run_b4_transport import (
    BOOT_BASE, BOOTSTRAP, LOADER_JSON, _attach_punch, _detach_punch,
)
from run_kl11_poll import decoded_instructions
from run_stage3_gold import ROOT, TraceWord, parse_trace
from run_stage4a import PDP7, Session
from run_stage4b import clean_cat


SYSTEM_SOURCES = {
    "boot": ROOT / "src/pdp11/unix/boot.s",
    "trap": ROOT / "src/pdp11/unix/trap.s",
    "init": ROOT / "src/pdp11/unix/init.s",
    "files": ROOT / "src/pdp11/unix/files.s",
    "control": ROOT / "src/pdp11/unix/control.s",
    "open": ROOT / "src/pdp11/unix/open.s",
    "read": ROOT / "src/pdp11/unix/read.s",
    "blocks": ROOT / "src/pdp11/unix/blocks.s",
    "write": ROOT / "src/pdp11/unix/write.s",
}
NATIVE_STEMS = {
    "boot": "uboot",
    "trap": "utrap",
    "init": "uinit",
    "files": "ufiles",
    "control": "uctrl",
    "open": "uopen",
    "read": "uread",
    "blocks": "ublks",
    "write": "uwrite",
}
CAT_SOURCE = ROOT / "src/pdp11/cmd/cat.s"
EVIDENCE = ROOT / "evidence/core-cat"
ERA = ROOT / "eras/pdp7-crossdev"
SYSTEM_TAPES = {
    name: ROOT / f"artifacts/core-unix-{name}.ptap"
    for name in SYSTEM_SOURCES
}
CAT_TAPE = ROOT / "artifacts/cat.ptap"
EXPECTED = "PDP-11 Unix read this from readme.\r\n"
ENTRY = 0o001000
LABEL_RE = re.compile(r"^l ([a-z_][a-z0-9_]{0,7}) ([0-7]{6})$")


def labels_from_trace(trace: str) -> dict[str, int]:
    labels: dict[str, int] = {}
    for line in trace.splitlines():
        match = LABEL_RE.fullmatch(line)
        if match:
            name, address = match.groups()
            value = int(address, 8)
            if name in labels and labels[name] != value:
                raise ValueError(f"conflicting native label {name}")
            labels[name] = value
    return labels


def validate_native(system: tuple[TraceWord, ...], cat: tuple[TraceWord, ...],
                    labels: dict[str, int]) -> None:
    """Check native words with the oracle and enforce the intended layout."""
    for records in (system, cat):
        decoded_instructions(records)
    system_addresses = {item.address for item in system}
    cat_addresses = {item.address for item in cat}
    if system_addresses & cat_addresses:
        raise ValueError("system and cat native maps overlap")
    required = {
        "start", "trapent", "fsinit", "namei", "iget", "access",
        "fassign", "pget", "bread", "sysopen", "sysread", "syswrit",
        "sysclos", "sysexit", "state", "fds", "blockbuf",
    }
    if missing := required - labels.keys():
        raise ValueError(f"native system trace lacks labels: {sorted(missing)}")
    mnemonics = {
        item.mnemonic for item in decoded_instructions(system + cat)
    }
    if missing := {"SUB", "BEQ", "DEC", "TRAP", "RTI"} - mnemonics:
        raise ValueError(f"system lacks required native instructions: {sorted(missing)}")
    cat_text = CAT_SOURCE.read_text(encoding="ascii")
    if "PDP-11 Unix read this" in cat_text:
        raise ValueError("cat contains the readme output instead of reading the file")


def fast_script(system: tuple[TraceWord, ...], cat: tuple[TraceWord, ...]) -> str:
    lines = [
        "; Fast debugging only: every target word came from native PDP-7 as11.",
        "do machines/pdp11/pdp11.simh",
    ]
    for item in sorted(system + cat, key=lambda value: value.address):
        lines.append(f"deposit {item.address:06o} {item.word:06o}")
    lines.append("echo CORE UNIX CAT START")
    lines.extend((f"go {ENTRY:06o}", ""))
    return "\n".join(lines)


def _command(child: pexpect.spawn, command: str) -> str:
    child.sendline(command)
    child.expect_exact("sim>")
    return child.before.replace("\r", "")


def _examine(child: pexpect.spawn, address: int) -> int:
    text = _command(child, f"examine {address:06o}")
    match = re.search(rf"{address:o}:\s+([0-7]{{6}})", text)
    if not match:
        raise RuntimeError(f"cannot parse memory at {address:06o}: {text!r}")
    return int(match.group(1), 8)


def check_result(child: pexpect.spawn, labels: dict[str, int]) -> None:
    state = labels["state"]
    expected = {
        state + 0o20: 2,
        state + 0o22: len(EXPECTED),
        state + 0o24: 5,
        state + 0o26: 5,
        state + 0o30: 1,
        state + 0o4: 0o177770,
        state + 0o6: 0o177740,
    }
    for address, value in expected.items():
        observed = _examine(child, address)
        if observed != value:
            raise RuntimeError(
                f"memory {address:06o}={observed:06o}, expected {value:06o}"
            )
    for offset in (0, 0o6, 0o14):
        if _examine(child, labels["fds"] + offset) != 0:
            raise RuntimeError("exit did not close fd 0, fd 1, and cat's fd 2")
    if (_examine(child, 0o042000) != 0o042120 or
            _examine(child, 0o042042) != 0o005015):
        raise RuntimeError("readme bytes are not present in RAM filesystem block 2")
    if (_examine(child, labels["blockbuf"]) != 0o042120 or
            _examine(child, labels["blockbuf"] + 0o42) != 0o005015):
        raise RuntimeError("bread did not copy readme through the kernel block buffer")


def execute_fast(system: tuple[TraceWord, ...], cat: tuple[TraceWord, ...],
                 labels: dict[str, int], record: bool) -> str:
    transcript = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="core-cat-fast-") as directory:
        script = Path(directory) / "core-cat.simh"
        script.write_text(fast_script(system, cat), encoding="ascii")
        child = pexpect.spawn("pdp11", [str(script)], cwd=str(ROOT),
                              encoding="latin1", timeout=30)
        child.logfile_read = transcript
        try:
            child.expect_exact("CORE UNIX CAT START")
            outcome = child.expect_exact((EXPECTED, "HALT instruction"), timeout=30)
            if outcome == 1:
                child.expect_exact("sim>")
                state = labels["state"]
                diagnostic = {
                    f"{state + offset:06o}": _examine(child, state + offset)
                    for offset in (0, 0o20, 0o22, 0o24, 0o26, 0o30)
                }
                diagnostic.update({
                    f"{labels['fds'] + offset:06o}":
                        _examine(child, labels["fds"] + offset)
                    for offset in (0, 0o4, 0o6, 0o12, 0o14, 0o20)
                })
                diagnostic.update({
                    f"{address:06o}": _examine(child, address)
                    for address in tuple(range(0o041000, 0o041036, 2))
                    + tuple(range(0o030060, 0o030070, 2))
                })
                raise RuntimeError(
                    "cat halted before output; memory="
                    + ", ".join(
                        f"{address}:{value:06o}"
                        for address, value in diagnostic.items()
                    )
                )
            child.expect_exact("HALT instruction", timeout=20)
            child.expect_exact("sim>")
            check_result(child, labels)
            child.sendline("quit")
            child.expect(pexpect.EOF, timeout=10)
        finally:
            if child.isalive():
                child.close(force=True)
    text = transcript.getvalue().replace("\r", "")
    if record:
        (EVIDENCE / "fast-pdp11.transcript.txt").write_text(text, encoding="latin1")
    return text


def _pdp7_session(directory: Path, account: str,
                  transcript: io.StringIO) -> tuple[pexpect.spawn, Session]:
    child = pexpect.spawn(str(PDP7), ["pdp7.simh"], cwd=str(directory),
                          encoding="latin1", timeout=30)
    child.logfile_read = transcript
    native = Session(child)
    child.expect_exact("login:")
    native.line(account)
    child.expect_exact("password:")
    native.line(account)
    child.expect_exact("@ ")
    return child, native


def _close_pdp7(child: pexpect.spawn) -> None:
    if child.isalive():
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _clean_transcript(text: str) -> str:
    """Remove terminal carriage returns and prompt-end spaces from evidence."""
    return "\n".join(
        line.rstrip() for line in text.replace("\r", "").splitlines()
    ) + "\n"


def build_on_working_copy(record: bool, punch: bool) -> tuple[dict[str, str], str]:
    """Assemble and optionally punch on a disposable copy of the era disk."""
    canonical_hash = _sha256(ERA / "pdp7.fs")
    transcript = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="core-cat-pdp7-") as directory:
        temporary = Path(directory)
        for name in ("pdp7.simh", "pdp7.fs", "boot.rim"):
            shutil.copy2(ERA / name, temporary / name)

        child, native = _pdp7_session(temporary, "shankao", transcript)
        try:
            native_sources = {
                f"{NATIVE_STEMS[name]}.s": source
                for name, source in SYSTEM_SOURCES.items()
            }
            native_sources["ucat.s"] = CAT_SOURCE
            for native_name, source in native_sources.items():
                native.command(f"rm {native_name}")
                native.install(native_name, source.read_text(encoding="ascii"))
            for output in tuple(
                    f"{NATIVE_STEMS[name]}.o" for name in SYSTEM_SOURCES
                    ) + ("ucat.o",):
                native.command(f"rm {output}")
            system_traces: dict[str, str] = {}
            for name in SYSTEM_SOURCES:
                stem = NATIVE_STEMS[name]
                result = native.command(f"as11 {stem}.s {stem}.o", timeout=900)
                if "?" in result or re.search(r"(?:^|\n)e [0-7]{6} ", result):
                    raise RuntimeError(
                        f"native as11 failed on Unix {name}: {result!r}")
            result = native.command("as11 ucat.s ucat.o", timeout=900)
            if "?" in result or re.search(r"(?:^|\n)e [0-7]{6} ", result):
                raise RuntimeError("native as11 failed on cat")
            for name in SYSTEM_SOURCES:
                stem = NATIVE_STEMS[name]
                system_traces[name] = clean_cat(
                    native.command(f"cat {stem}.o", timeout=300)
                )
                if not system_traces[name]:
                    raise RuntimeError(f"native as11 emitted no Unix {name} output")
                if re.search(r"(?:^|\n)e [0-7]{6} ", system_traces[name]):
                    raise RuntimeError(
                        f"native as11 recorded an error for Unix {name}: "
                        f"{system_traces[name]!r}")
            cat_trace = clean_cat(native.command("cat ucat.o", timeout=300))
            if not cat_trace:
                raise RuntimeError("native as11 emitted no cat output")
            if re.search(r"(?:^|\n)e [0-7]{6} ", cat_trace):
                raise RuntimeError(
                    f"native as11 recorded an error for cat: {cat_trace!r}")
        finally:
            _close_pdp7(child)

        if punch:
            child, native = _pdp7_session(temporary, "system", transcript)
            linked_names: list[str] = []
            try:
                outputs = tuple(
                    f"{NATIVE_STEMS[name]}.o" for name in SYSTEM_SOURCES
                ) + ("ucat.o",)
                for name in outputs + ("abspun",):
                    native.command(f"rm {name}")
                    if "?" in native.command(f"ln shankao {name}"):
                        raise RuntimeError(f"system could not link shankao/{name}")
                    linked_names.append(name)
                tapes = tuple(
                    (f"{NATIVE_STEMS[name]}.o", SYSTEM_TAPES[name])
                    for name in SYSTEM_SOURCES
                ) + (("ucat.o", CAT_TAPE),)
                for name, destination in tapes:
                    punched = temporary / destination.name
                    _attach_punch(child, punched)
                    result = native.command(f"abspun {name} uxout", timeout=900)
                    _detach_punch(child)
                    if "?" in result:
                        raise RuntimeError(f"native punch failed for {name}")
                    destination.write_bytes(punched.read_bytes())
            finally:
                for name in reversed(linked_names):
                    native.command(f"rm {name}")
                native.command("rm uxout")
                _close_pdp7(child)

        if _sha256(ERA / "pdp7.fs") != canonical_hash:
            raise RuntimeError("normal Unix build changed the canonical crossdev image")

    if record:
        (EVIDENCE / "pdp7-build-punch.transcript.txt").write_text(
            _clean_transcript(transcript.getvalue()), encoding="latin1")
        (EVIDENCE / "pdp7-working-copy.txt").write_text(
            f"canonical_image={ERA.relative_to(ROOT) / 'pdp7.fs'}\n"
            f"canonical_sha256_before={canonical_hash}\n"
            f"canonical_sha256_after={_sha256(ERA / 'pdp7.fs')}\n"
            "build_image=disposable copy\n",
            encoding="utf-8")
    return system_traces, cat_trace


def rebuild_parts(parts: tuple[str, ...], record: bool) -> dict[str, str]:
    """Rebuild selected system parts on a disposable disk for debugging."""
    canonical_hash = _sha256(ERA / "pdp7.fs")
    transcript = io.StringIO()
    traces: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="core-cat-parts-") as directory:
        temporary = Path(directory)
        for name in ("pdp7.simh", "pdp7.fs", "boot.rim"):
            shutil.copy2(ERA / name, temporary / name)
        child, native = _pdp7_session(temporary, "shankao", transcript)
        try:
            for name in parts:
                stem = NATIVE_STEMS[name]
                native.command(f"rm {stem}.s")
                native.install(
                    f"{stem}.s", SYSTEM_SOURCES[name].read_text(encoding="ascii")
                )
                native.command(f"rm {stem}.o")
                result = native.command(f"as11 {stem}.s {stem}.o", timeout=900)
                if "?" in result or re.search(r"(?:^|\n)e [0-7]{6} ", result):
                    raise RuntimeError(
                        f"native as11 failed on Unix {name}: {result!r}")
                trace = clean_cat(native.command(f"cat {stem}.o", timeout=300))
                if not trace or re.search(r"(?:^|\n)e [0-7]{6} ", trace):
                    raise RuntimeError(
                        f"bad native as11 output for Unix {name}: {trace!r}")
                traces[name] = trace
        finally:
            _close_pdp7(child)
        if _sha256(ERA / "pdp7.fs") != canonical_hash:
            raise RuntimeError("partial rebuild changed the canonical crossdev image")
    if record:
        joined = "-".join(parts)
        (EVIDENCE / f"pdp7-rebuild-{joined}.transcript.txt").write_text(
            _clean_transcript(transcript.getvalue()), encoding="latin1"
        )
    return traces


def verify_tape(path: Path, records: tuple[TraceWord, ...]) -> tuple[int, int]:
    memory, transfer, count = parse_absolute(path.read_bytes())
    expected = {item.address: item.word for item in records}
    if words_from_bytes(memory) != expected:
        raise ValueError(f"{path.name} differs from native as11 output")
    if transfer != 1:
        raise ValueError(f"{path.name} has transfer address {transfer!r}, not 1")
    return count, len(path.read_bytes())


def historical_load(system_parts: dict[str, tuple[TraceWord, ...]],
                    cat: tuple[TraceWord, ...],
                    labels: dict[str, int], record: bool) -> str:
    """Load the DEC loader and both payload tapes through the real PTR."""
    transcript = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="core-cat-loader-") as directory:
        loader = Path(directory) / "DEC-11-L2PC-PO.ptap"
        loader.write_bytes(loader_bytes(LOADER_JSON))
        child = pexpect.spawn("pdp11", cwd=str(ROOT), encoding="latin1", timeout=30)
        child.logfile_read = transcript
        try:
            _command(child, "do machines/pdp11/pdp11.simh")
            _command(child, "set ptr enabled")
            _command(child, f"attach ptr {loader}")
            for index, word in enumerate(BOOTSTRAP):
                _command(child, f"deposit {BOOT_BASE + 2 * index:06o} {word:06o}")
            child.sendline(f"go {BOOT_BASE:06o}")
            child.expect_exact("HALT instruction", timeout=20)
            child.expect_exact("sim>")
            loads = tuple(
                (SYSTEM_TAPES[name], system_parts[name])
                for name in SYSTEM_SOURCES
            ) + ((CAT_TAPE, cat),)
            for tape, records in loads:
                _command(child, "detach ptr")
                _command(child, f"attach ptr {tape}")
                child.sendline("go 057500")
                child.expect_exact("HALT instruction", timeout=60)
                child.expect_exact("sim>")
                for item in records:
                    if _examine(child, item.address) != item.word:
                        raise RuntimeError(
                            f"PTR load differs at {item.address:06o} in {tape.name}")
            child.sendline(f"go {ENTRY:06o}")
            child.expect_exact(EXPECTED, timeout=30)
            child.expect_exact("HALT instruction", timeout=20)
            child.expect_exact("sim>")
            check_result(child, labels)
            child.sendline("quit")
            child.expect(pexpect.EOF, timeout=10)
        finally:
            if child.isalive():
                child.close(force=True)
    text = transcript.getvalue().replace("\r", "")
    if record:
        (EVIDENCE / "paper-tape-pdp11.transcript.txt").write_text(
            text, encoding="latin1")
    return text


def run(record: bool, reuse_traces: bool, skip_tape: bool,
        parts: tuple[str, ...] = ()) -> None:
    if record:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
    if parts:
        rebuilt = rebuild_parts(parts, record)
        system_traces = {
            name: (EVIDENCE / f"{name}-native-trace.txt").read_text(
                encoding="ascii"
            ) for name in SYSTEM_SOURCES if name not in rebuilt
        }
        system_traces.update(rebuilt)
        cat_trace = (EVIDENCE / "cat-native-trace.txt").read_text(encoding="ascii")
        if record:
            for name in parts:
                (EVIDENCE / f"{name}-native-trace.txt").write_text(
                    system_traces[name], encoding="ascii"
                )
    elif reuse_traces:
        system_traces = {
            name: (EVIDENCE / f"{name}-native-trace.txt").read_text(
                encoding="ascii"
            ) for name in SYSTEM_SOURCES
        }
        cat_trace = (EVIDENCE / "cat-native-trace.txt").read_text(encoding="ascii")
    else:
        system_traces, cat_trace = build_on_working_copy(record, not skip_tape)
        if record:
            for name, trace in system_traces.items():
                (EVIDENCE / f"{name}-native-trace.txt").write_text(
                    trace, encoding="ascii")
            (EVIDENCE / "cat-native-trace.txt").write_text(
                cat_trace, encoding="ascii")
    system_trace = "".join(system_traces.values())
    system_parts = {
        name: parse_trace(trace) for name, trace in system_traces.items()
    }
    system, cat = parse_trace(system_trace), parse_trace(cat_trace)
    labels = labels_from_trace(system_trace)
    validate_native(system, cat, labels)
    execute_fast(system, cat, labels, record)

    tape_counts: dict[str, tuple[int, int]] = {}
    if not skip_tape:
        if reuse_traces:
            # Existing tapes are accepted only if they match the reused native
            # traces.  A changed source must run the disposable PDP-7 build.
            pass
        for name, trace in system_traces.items():
            tape_counts[name] = verify_tape(
                SYSTEM_TAPES[name], parse_trace(trace)
            )
        tape_counts["cat"] = verify_tape(CAT_TAPE, cat)
        historical_load(system_parts, cat, labels, record)

    system_instructions = sum(item.kind == "i" for item in system)
    cat_instructions = sum(item.kind == "i" for item in cat)
    detail = ""
    if tape_counts:
        detail = " " + " ".join(
            [f"{name}_tape={tape_counts[name][1]}"
             for name in SYSTEM_SOURCES]
            + [f"cat_tape={tape_counts['cat'][1]}"]
        )
    print(
        f"PASS output={EXPECTED!r} system_words={len(system)}"
        f" system_instructions={system_instructions} cat_words={len(cat)}"
        f" cat_instructions={cat_instructions}{detail}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--reuse-traces", action="store_true")
    parser.add_argument("--skip-tape", action="store_true")
    parser.add_argument("--parts", nargs="+", choices=tuple(SYSTEM_SOURCES))
    args = parser.parse_args()
    if args.parts and not args.skip_tape:
        parser.error("--parts is a fast debugging build; use --skip-tape")
    run(args.record, args.reuse_traces, args.skip_tape, tuple(args.parts or ()))


if __name__ == "__main__":
    main()
