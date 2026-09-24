# SPDX-License-Identifier: GPL-3.0-only
"""Prepare the recovered B runtime for the current as11 command."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECOVERED_RUNTIME = ROOT / "machines/pdp7/pdp7-unix/src/cmd/bl.s"


def as11_runtime() -> str:
    """Return the recovered runtime with 16-word as11 I/O buffers."""
    text = RECOVERED_RUNTIME.read_text(encoding="ascii")
    replacements = {
        "sys read; ibufp: ..; 64": "sys read; ibufp: ..; 16",
        "sys write; obufp: ..; 64": "sys write; obufp: ..; 16",
    }
    for before, after in replacements.items():
        if text.count(before) != 1:
            raise RuntimeError(f"unexpected recovered B runtime text: {before}")
        text = text.replace(before, after)
    if text.count("\n   -64\n") != 2:
        raise RuntimeError("unexpected recovered B runtime buffer allocation")
    return text.replace("\n   -64\n", "\n   -16\n")
