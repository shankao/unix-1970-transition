# SPDX-License-Identifier: GPL-3.0-only
"""Deliberately update and verify as11 in the living PDP-7 crossdev era.

This is a toolchain installation command, not part of normal Unix builds.
"""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import re

import pexpect

from run_stage4a import PDP7, Session
from run_stage4b import assembler_failed, clean_cat
from run_stage3_gold import ROOT
from as11_runtime import as11_runtime


ERA = ROOT / "eras/pdp7-crossdev"
IMAGE = ERA / "pdp7.fs"
SOURCE = ROOT / "src/pdp7/as11/as11.b"
CHECK = ROOT / "tests/pdp7-as11/unix-encoding.s"
LONG_CHECK = ROOT / "tests/pdp7-as11/stage4b-positive.s"
LONG_CHECK_SHA256 = "315bb66cc17fb30a9c7b5077c18301a3b8924e49f6dd08d30743acb0efbed19a"
ENCODING_CHECK = ROOT / "tests/pdp7-as11/stage4c-encoding.s"
ENCODING_CHECK_SHA256 = "c0845ce5d60d0df3a3121a186ea959ac703a5f259238ac3ab80ba756ac5000a7"
REAL_CHECK = ROOT / "tests/pdp7-as11/stage4c-stage3-shaped.s"
REAL_CHECK_SHA256 = "b5fd769763519fd73e97de578fe2691dd606193fcfd0ee71c075916f174117ae"
GOLD_CHECK = ROOT / "tests/pdp7-as11/stage3b-gold.s"
GOLD_EXPECTED = ROOT / "evidence/stage3-gold/native-trace.txt"
README = ROOT / "src/pdp7/as11/readme.corecat"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install_large(native: Session, name: str, text: str) -> None:
    native.line("ed"); native.child.expect_exact("edit")
    native.line("a")
    for line in text.splitlines():
        if "#" in line or "@" in line:
            raise ValueError(f"tty editing character in {name}: {line!r}")
        native.line(line)
    native.line(".")
    native.line(f"w {name}")
    native.child.expect(r"[0-9]+\r?\n", timeout=300)
    native.line("q"); native.child.expect_exact("@ ", timeout=30)


def run(reuse_runtime: bool = False) -> None:
    before_hash = sha256(IMAGE)
    transcript = io.StringIO()
    child = pexpect.spawn(str(PDP7), ["pdp7.simh"], cwd=str(ERA),
                          encoding="latin1", timeout=30)
    child.logfile_read = transcript
    native = Session(child)
    try:
        child.expect_exact("login:"); native.line("shankao")
        child.expect_exact("password:"); native.line("shankao")
        child.expect_exact("@ ")
        current = clean_cat(native.command("cat as11.b", timeout=300))
        if current != SOURCE.read_text(encoding="ascii").lower():
            expected = ("nlocal >= 10", "while(i<21)", "mtab[63]",
                        "0164162,0141160,0104400;")
            extended = ("while(i<24)", "mtab[72]", "0163165,0142000,0160000",
                        "0142145,0161000,001400", "0144145,0143000,005300")
            if (not all(text in current for text in expected)
                    and not all(text in current for text in extended)):
                raise RuntimeError("era as11.b is not the expected pre-Unix source")
            native.command("rm as11.b")
            install_large(native, "as11.b", SOURCE.read_text(encoding="ascii"))

        # Keep the recovered runtime logic, but use smaller buffers for this
        # assembler.  The linked Unix mnemonics otherwise consume the stack
        # margin measured for Stage 4C.  Ten local definitions remain the
        # accepted limit.  as11.b puts both symbol tables in space released
        # below these smaller buffers; the checks below verify that layout.
        if not reuse_runtime:
            native.command("rm s4bl.s")
            install_large(native, "s4bl.s", as11_runtime())

        native.command("rm as11.s")
        native.command("rm a.out")
        compiled = native.command("b as11.b as11.s", timeout=900)
        if "?" in compiled or re.search(
                r"(?:^|[\r\n])(?:[a-z]{2}|\[\]|\(\)) [0-9]+", compiled):
            raise RuntimeError("native B compilation of as11 failed: " + repr(compiled))
        linked = native.command(
            "as s4op.s s4bl.s as11.s rewind.s s4bi.s", timeout=900)
        if assembler_failed(linked):
            raise RuntimeError("native assembly/link of as11 failed")
        native.command("rm unix.s")
        native.install("unix.s", CHECK.read_text(encoding="ascii"))
        native.command("rm unix.o")
        if "?" in native.command("a.out unix.s unix.o", timeout=300):
            raise RuntimeError("updated as11 failed its Unix instruction test")
        observed = clean_cat(native.command("cat unix.o", timeout=120))
        expected = (
            "i 001000 160203\n"
            "i 001002 001401\n"
            "i 001004 005304\n"
            "l done 001006\n"
            "i 001006 000000\n"
        )
        if observed != expected:
            raise RuntimeError(f"unexpected native Unix encodings: {observed!r}")
        # Test a named copy before replacing the installed command.  PDP-7 ln
        # preserves the source name; it cannot give a.out a new name.
        native.command("rm asnew")
        if "?" in native.command("cp a.out asnew", timeout=300):
            raise RuntimeError("could not copy the verified as11 executable")
        native.command("rm unix2.o")
        if "?" in native.command("asnew unix.s unix2.o", timeout=300):
            raise RuntimeError("linked as11 command failed its Unix test")
        linked = clean_cat(native.command("cat unix2.o", timeout=120))
        if linked != expected:
            raise RuntimeError(f"linked as11 emitted unexpected data: {linked!r}")

        # The four-line instruction check fits in one B input buffer.  Also
        # exercise a source file that crosses a refill boundary before making
        # this executable the era's installed assembler.
        native.command("rm long.s")
        native.install("long.s", LONG_CHECK.read_text(encoding="ascii"))
        native.command("rm long.o")
        if "?" in native.command("asnew long.s long.o", timeout=300):
            raise RuntimeError("linked as11 failed its long-input test")
        long_output = clean_cat(native.command("cat long.o", timeout=180))
        if hashlib.sha256(long_output.encode("ascii")).hexdigest() != LONG_CHECK_SHA256:
            raise RuntimeError("linked as11 failed its long-input comparison")

        native.command("rm enc.s")
        native.install("enc.s", ENCODING_CHECK.read_text(encoding="ascii"))
        native.command("rm enc.o")
        if "?" in native.command("asnew enc.s enc.o", timeout=600):
            raise RuntimeError("linked as11 failed its addressing-mode test")
        enc_output = clean_cat(native.command("cat enc.o", timeout=300))
        if hashlib.sha256(enc_output.encode("ascii")).hexdigest() != ENCODING_CHECK_SHA256:
            raise RuntimeError("linked as11 failed its addressing-mode comparison")

        native.command("rm real.s")
        native.install("real.s", REAL_CHECK.read_text(encoding="ascii"))
        native.command("rm real.o")
        if "?" in native.command("asnew real.s real.o", timeout=600):
            raise RuntimeError("linked as11 failed its realistic workload test")
        real_output = clean_cat(native.command("cat real.o", timeout=300))
        if hashlib.sha256(real_output.encode("ascii")).hexdigest() != REAL_CHECK_SHA256:
            raise RuntimeError("linked as11 failed its realistic workload comparison")

        # The shorter Stage-3-shaped check did not expose the final forward
        # reference in the accepted 1,408-byte gold source.  Test that exact
        # program before installing the command.
        native.command("rm gold.s")
        native.install("gold.s", GOLD_CHECK.read_text(encoding="ascii"))
        native.command("rm gold.o")
        if "?" in native.command("asnew gold.s gold.o", timeout=900):
            raise RuntimeError("linked as11 failed the exact Stage-3 gold source")
        gold_output = clean_cat(native.command("cat gold.o", timeout=300))
        if gold_output != GOLD_EXPECTED.read_text(encoding="ascii"):
            raise RuntimeError("linked as11 changed the Stage-3 gold trace")

        # rn unlinks the destination and invokes the PDP-7 rename syscall, so
        # the already-tested staging file becomes the installed command.
        if "?" in native.command("rn asnew as11", timeout=300):
            raise RuntimeError("could not rename the verified as11 command")
        native.command("rm final.o")
        if "?" in native.command("as11 long.s final.o", timeout=300):
            raise RuntimeError("installed as11 failed its long-input test")
        final_output = clean_cat(native.command("cat final.o", timeout=180))
        if hashlib.sha256(final_output.encode("ascii")).hexdigest() != LONG_CHECK_SHA256:
            raise RuntimeError("installed as11 failed its long-input comparison")
        native.command("rm readme")
        native.install("readme", README.read_text(encoding="ascii"))
        native.command("rm a.out")
        native.command("rm unix2.o")
        native.command("rm long.o")
        native.command("rm enc.o")
        native.command("rm real.o")
        native.command("rm gold.o")
        native.command("rm final.o")
        if "?" in native.command("stat as11 abspun", timeout=120):
            raise RuntimeError("installed as11 or accepted abspun is missing")
    finally:
        child.sendcontrol("e"); child.expect_exact("sim>", timeout=10)
        child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)
    print(f"PASS before={before_hash} after={sha256(IMAGE)}")


def inspect(source: bool) -> None:
    child = pexpect.spawn(str(PDP7), ["pdp7.simh"], cwd=str(ERA),
                          encoding="latin1", timeout=30)
    native = Session(child)
    try:
        child.expect_exact("login:"); native.line("shankao")
        child.expect_exact("password:"); native.line("shankao")
        child.expect_exact("@ ")
        print(clean_cat(native.command("stat as11 as11.b s4bl.s", timeout=120)), end="")
        if source:
            print(clean_cat(native.command("cat as11.b", timeout=300)), end="")
    finally:
        child.sendcontrol("e"); child.expect_exact("sim>", timeout=10)
        child.sendline("quit"); child.expect(pexpect.EOF, timeout=10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspect-source", action="store_true")
    parser.add_argument("--inspect-stat", action="store_true")
    parser.add_argument("--reuse-runtime", action="store_true")
    args = parser.parse_args()
    if args.inspect_source or args.inspect_stat:
        inspect(args.inspect_source)
    else:
        run(args.reuse_runtime)
