# Modern Verification Tools

Everything in this directory is class M unless explicitly documented otherwise.

These tools exist to verify encodings, inspect tapes, automate reproducibility checks, and reduce emulator debugging loops. They are not part of the historical code-generation path.

# Modern host-side tools

- `pdp11_oracle.py`: class-M encoder/decoder and byte/branch oracle for the
  project's base KA11/PDP-11/20 instruction subset. See
  `docs/PDP11-ORACLE.md`.
