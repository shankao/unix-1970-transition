#!/usr/bin/env python3
"""Build and run the native Stage 4B B symbol engine on machines/pdp7."""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import re

import pexpect

from run_stage4a import ROOT, BUILD, IMAGE, Session, git_status, sha256


AS11_B = ROOT / "src/pdp7/as11/as11.b"
REWIND = ROOT / "src/pdp7/as11/rewind.s"
CASES = {
    "empty.s": ROOT / "tests/pdp7-as11/empty.s",
    "pos.s": ROOT / "tests/pdp7-as11/stage4b-positive.s",
    "large.s": ROOT / "tests/pdp7-as11/stage4b-substantial.s",
    "undef.s": ROOT / "tests/pdp7-as11/undefined.s",
    "dup.s": ROOT / "tests/pdp7-as11/duplicate.s",
    "conf.s": ROOT / "tests/pdp7-as11/conflict.s",
    "missf.s": ROOT / "tests/pdp7-as11/missingf.s",
    "missb.s": ROOT / "tests/pdp7-as11/missingb.s",
    "badloc.s": ROOT / "tests/pdp7-as11/badlocal.s",
    "badexp.s": ROOT / "tests/pdp7-as11/badexpr.s",
    "unl.s": ROOT / "tests/pdp7-as11/unmatchedl.s",
    "unr.s": ROOT / "tests/pdp7-as11/unmatchedr.s",
    "badoct.s": ROOT / "tests/pdp7-as11/badoctal.s",
    "odd.s": ROOT / "tests/pdp7-as11/oddword.s",
    "over.s": ROOT / "tests/pdp7-as11/addrover.s",
    "urdot.s": ROOT / "tests/pdp7-as11/unresdot.s",
}

# Fixed expected hashes for PDP-7-created semantic traces.  These are comparison
# vectors, not a host implementation of the language or symbol semantics.
EXPECTED_SHA256 = {
    "empty.s": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "pos.s": "315bb66cc17fb30a9c7b5077c18301a3b8924e49f6dd08d30743acb0efbed19a",
    "large.s": "dc9bbf9cf426b16cbfc482dd462f3b17d6a2c3edcacf44284baa6adebecb1eef",
    "undef.s": "531d34ea9ad83edee6d8375c17d2672c0000237f2076c7011eb5a03785309675",
    "dup.s": "b8ce8f5ab2d757e67c3cee46996036657ec58d6eadeba65b7f32b919b1885b30",
    "conf.s": "b8ce8f5ab2d757e67c3cee46996036657ec58d6eadeba65b7f32b919b1885b30",
    "missf.s": "531d34ea9ad83edee6d8375c17d2672c0000237f2076c7011eb5a03785309675",
    "missb.s": "531d34ea9ad83edee6d8375c17d2672c0000237f2076c7011eb5a03785309675",
    "badloc.s": "ecf82dbe9d04dd79a88b6e6f62c7067e522dbcb56d798416c5975cd70be020cb",
    "badexp.s": "2ec3412c8856ab996824fae9d03eafe8a9b355d0139b36c2a09f38cae220ac0d",
    "unl.s": "fa1c527b98683c2226d62bad699ca025a458f678fbbbad67cb938d109c27cb20",
    "unr.s": "e481f4acf20f4b947cf0bedafd103ebbfb7c7aa53309846e46dcc3292d4e822e",
    "badoct.s": "2ec3412c8856ab996824fae9d03eafe8a9b355d0139b36c2a09f38cae220ac0d",
    "odd.s": "0ceca1c4c0b0c56b116a60fb73d535ef9f6fa94003669537075ce1575a431640",
    "over.s": "496ee5678054b8395573c7a6c4b18055f05eed836e6b582753b25c6cdbac5237",
    "urdot.s": "fe3524b3c8c232b47eeebd88e5ba4acbd36301a61aaf4937c7ba7362c984e5c1",
}


def clean_cat(raw: str) -> str:
    value = raw.replace("\r", "").replace("\x00", "")
    return value[1:] if value.startswith("\n") else value


def assembler_failed(output: str) -> bool:
    return (
        "?" in output
        or "I" not in output
        or "II" not in output
        or re.search(r"(?:^|[\r\n])[a-z] [0-9]{4}(?:[\r\n]|$)", output)
        is not None
    )


def run(record: bool, build_only: bool, reuse_source: bool,
        functional_only: bool = False) -> None:
    pre_status = git_status()
    pre_hash = sha256(IMAGE)
    transcript = io.StringIO()
    evidence = ROOT / "evidence/stage4b"
    evidence.mkdir(parents=True, exist_ok=True)
    child = pexpect.spawn(
        str(BUILD / "pdp7"), ["unixv0.simh"], cwd=str(BUILD),
        encoding="latin1", timeout=30,
    )
    child.logfile_read = transcript
    session = Session(child)
    failure: Exception | None = None
    stats = ""
    try:
        child.expect_exact("login:")
        session.line("shankao")
        child.expect_exact("password:")
        session.line("shankao")
        child.expect_exact("@ ")

        if not reuse_source:
            session.command("rm as11.b")
            session.install("as11.b", AS11_B.read_text(encoding="ascii"))
        session.command("rm as11.s")
        session.command("rm a.out")
        session.command("rm rewind.s")
        session.install("rewind.s", REWIND.read_text(encoding="ascii"))
        compile_output = session.command("b as11.b as11.s", timeout=600)
        if "?" in compile_output or re.search(
            r"(?:^|[\r\n])(?:[a-z]{2}|\[\]|\(\)) [0-9]+", compile_output
        ):
            raise RuntimeError("native B compilation failed: " + repr(compile_output))
        link_output = session.command(
            "as s4op.s s4bl.s as11.s rewind.s s4bi.s", timeout=600
        )
        if assembler_failed(link_output):
            raise RuntimeError("native assembly/link failed: " + repr(link_output))
        stats = session.command("stat as11.b as11.s a.out", timeout=120)

        if not build_only:
            cases = CASES.items()
            if functional_only:
                # Later encoder growth reduced the artificial 48/10 frontier;
                # retain that evidence while checking all language semantics.
                cases = ((name, path) for name, path in cases if name != "large.s")
            for native, host in cases:
                session.command(f"rm {native}")
                session.install(native, host.read_text(encoding="ascii"))
                out = native.split(".")[0] + ".o"
                session.command(f"rm {out}")
                result = session.command(f"a.out {native} {out}", timeout=600)
                if "?" in result:
                    raise RuntimeError(f"native execution failed for {native}")
                observed = clean_cat(session.command(f"cat {out}", timeout=180))
                digest = hashlib.sha256(observed.encode("ascii")).hexdigest()
                if digest != EXPECTED_SHA256[native]:
                    raise RuntimeError(
                        f"semantic trace mismatch for {native}: {digest}"
                    )
                (evidence / (native + ".out")).write_text(observed, encoding="ascii")
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
        evidence.mkdir(parents=True, exist_ok=True)
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--reuse-source", action="store_true")
    parser.add_argument("--functional-only", action="store_true")
    args = parser.parse_args()
    run(args.record, args.build_only, args.reuse_source, args.functional_only)


if __name__ == "__main__":
    main()
