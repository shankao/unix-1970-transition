#!/usr/bin/env python3
"""Build and run Stage 4C on authoritative machines/pdp7 (M tooling)."""

from __future__ import annotations

import argparse
import io
from pathlib import Path
import re

import pexpect

from run_stage4a import ROOT, BUILD, IMAGE, Session, git_status, sha256
from run_stage4b import assembler_failed, clean_cat, EXPECTED_SHA256 as S4B_SHA


AS11_B = ROOT / "src/pdp7/as11/as11.b"
REWIND = ROOT / "src/pdp7/as11/rewind.s"
NATIVE_README = ROOT / "src/pdp7/as11/readme.stage4c"
FIXTURES = ROOT / "tests/pdp7-as11"
EXPECTED_ENCODING = (FIXTURES / "stage4c-encoding.expected").read_text(encoding="ascii")

# Native names obey the PDP-7 fixed-width convention. Values are fixed host
# comparison vectors; scanner/parser/encoder semantics execute only in B.
CASES = {
    "enc.s": (FIXTURES / "stage4c-encoding.s", EXPECTED_ENCODING),
    "pos.s": (FIXTURES / "stage4b-positive.s", S4B_SHA["pos.s"]),
    "bop.s": (FIXTURES / "stage4c-badoperand.s", "e 000001 xp\n"),
    "breg.s": (FIXTURES / "stage4c-badregister.s", "e 000001 rg\n"),
    "bsyn.s": (FIXTURES / "stage4c-badsyntax.s", "e 000001 ea\n"),
    "bpar.s": (FIXTURES / "stage4c-missingparen.s", "e 000001 rp\n"),
    "bplus.s": (FIXTURES / "stage4c-plus.s", "e 000001 xp\n"),
    "bstar.s": (FIXTURES / "stage4c-star.s", "e 000001 xp\n"),
    "brodd.s": (FIXTURES / "stage4c-branchodd.s", "e 000002 br\n"),
    "brlow.s": (FIXTURES / "stage4c-branchlow.s", "e 000002 br\n"),
    "brhigh.s": (FIXTURES / "stage4c-branchhigh.s", "e 000002 br\n"),
    "bjmp.s": (FIXTURES / "stage4c-jmpreg.s", "e 000001 jm\n"),
    "bjsr.s": (FIXTURES / "stage4c-jsrreg.s", "e 000001 jm\n"),
    "bmul.s": (FIXTURES / "stage4c-mul.s", "e 000001 st\n"),
    "bdiv.s": (FIXTURES / "stage4c-div.s", "e 000001 st\n"),
    "bash.s": (FIXTURES / "stage4c-ash.s", "e 000001 st\n"),
    "bashc.s": (FIXTURES / "stage4c-ashc.s", "e 000001 st\n"),
    "bxor.s": (FIXTURES / "stage4c-xor.s", "e 000001 st\n"),
    "bsob.s": (FIXTURES / "stage4c-sob.s", "e 000001 st\n"),
    "bmark.s": (FIXTURES / "stage4c-markinst.s", "e 000001 st\n"),
    # Keep the maximum-capacity Stage 4B regression last so a resource
    # failure does not hide independent encoder/rejection evidence.
    "large.s": (FIXTURES / "stage4b-substantial.s", S4B_SHA["large.s"]),
}


def install_large(session: Session, name: str, text: str) -> None:
    """Use the proven editor protocol but allow a large native write to finish."""
    session.line("ed")
    session.child.expect_exact("edit")
    session.line("a")
    for line in text.splitlines():
        if "#" in line or "@" in line:
            raise ValueError(f"tty editing character in {name}: {line!r}")
        session.line(line)
    session.line(".")
    session.line(f"w {name}")
    session.child.expect(r"[0-9]+\r?\n", timeout=300)
    session.line("q")
    session.child.expect_exact("@ ", timeout=30)


def matches(observed: str, expected: str) -> bool:
    if expected.startswith("e ") or expected.startswith("l "):
        return observed == expected
    import hashlib
    return hashlib.sha256(observed.encode("ascii")).hexdigest() == expected


def run(record: bool, build_only: bool, reuse_source: bool) -> None:
    pre_status = git_status()
    pre_hash = sha256(IMAGE)
    transcript = io.StringIO()
    evidence = ROOT / "evidence/stage4c"
    evidence.mkdir(parents=True, exist_ok=True)
    stats = ""
    failure: Exception | None = None
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
        if not reuse_source:
            session.command("rm as11.b")
            install_large(session, "as11.b", AS11_B.read_text(encoding="ascii"))
        session.command("rm as11.s")
        session.command("rm a.out")
        session.command("rm rewind.s")
        session.install("rewind.s", REWIND.read_text(encoding="ascii"))
        compile_output = session.command("b as11.b as11.s", timeout=900)
        if "?" in compile_output or re.search(
            r"(?:^|[\r\n])(?:[a-z]{2}|\[\]|\(\)) [0-9]+", compile_output
        ):
            raise RuntimeError("native B compilation failed: " + repr(compile_output))
        link_output = session.command(
            "as s4op.s s4bl.s as11.s rewind.s s4bi.s", timeout=900
        )
        if assembler_failed(link_output):
            raise RuntimeError("native assembly/link failed: " + repr(link_output))
        stats = session.command("stat as11.b as11.s a.out", timeout=180)
        if not build_only:
            for native, (host, expected) in CASES.items():
                session.command(f"rm {native}")
                session.install(native, host.read_text(encoding="ascii"))
                out = native.split(".")[0] + ".o"
                session.command(f"rm {out}")
                result = session.command(f"a.out {native} {out}", timeout=600)
                if "?" in result:
                    raise RuntimeError(f"native execution failed for {native}")
                observed = clean_cat(session.command(f"cat {out}", timeout=180))
                if not matches(observed, expected):
                    raise RuntimeError(
                        f"trace mismatch for {native}: observed={observed!r}"
                    )
                if record:
                    (evidence / (native + ".out")).write_text(observed, encoding="ascii")
            session.command("rm readme")
            session.install("readme", NATIVE_README.read_text(encoding="ascii"))
    except Exception as exc:
        failure = exc
    finally:
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)

    post_hash = sha256(IMAGE)
    post_status = git_status()
    if record or failure is not None:
        (evidence / "session.transcript.txt").write_text(
            transcript.getvalue(), encoding="latin1"
        )
        (evidence / "image-state.txt").write_text(
            f"pre_sha256={pre_hash}\npost_sha256={post_hash}\n"
            "pre_git_status:\n" + pre_status + "post_git_status:\n" + post_status,
            encoding="utf-8",
        )
        (evidence / "native-stat.txt").write_text(stats, encoding="latin1")
        if failure is not None:
            (evidence / "failure-latest.txt").write_text(
                repr(failure) + "\n", encoding="utf-8"
            )
    if failure is not None:
        raise failure
    print(f"PASS pre_sha256={pre_hash} post_sha256={post_hash}")


def install_readme() -> None:
    """Install only the reviewed native Stage 4C checkpoint status file."""
    child = pexpect.spawn(
        str(BUILD / "pdp7"), ["unixv0.simh"], cwd=str(BUILD),
        encoding="latin1", timeout=30,
    )
    session = Session(child)
    try:
        child.expect_exact("login:")
        session.line("shankao")
        child.expect_exact("password:")
        session.line("shankao")
        child.expect_exact("@ ")
        session.command("rm readme")
        session.install("readme", NATIVE_README.read_text(encoding="ascii"))
        session.command("cat readme", timeout=60)
    finally:
        child.sendcontrol("e")
        child.expect_exact("sim>", timeout=10)
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=10)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--reuse-source", action="store_true")
    parser.add_argument("--install-readme-only", action="store_true")
    args = parser.parse_args()
    if args.install_readme_only:
        install_readme()
    else:
        run(args.record, args.build_only, args.reuse_source)


if __name__ == "__main__":
    main()
