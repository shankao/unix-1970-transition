# SPDX-License-Identifier: GPL-3.0-only
"""Materialize the archival DEC Absolute Loader tape for human era replay."""

from __future__ import annotations

import argparse
from pathlib import Path

from dec_abs import loader_bytes


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence/b4/DEC-11-L2PC-PO.json"
DEFAULT_OUTPUT = ROOT / "eras/pdp11-crossdev/dec-absolute-loader.ptap"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    data = loader_bytes(SOURCE)
    args.output.write_bytes(data)
    print(f"wrote {len(data)} bytes to {args.output}")


if __name__ == "__main__":
    main()
