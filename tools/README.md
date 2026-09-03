# Modern Verification Tools

Everything in this directory is class M unless explicitly documented otherwise.

These tools exist to verify encodings, inspect tapes, automate reproducibility checks, and reduce emulator debugging loops. They are not part of the historical code-generation path.

# Modern host-side tools

- `pdp11_oracle.py`: class-M encoder/decoder and byte/branch oracle for the
  project's base KA11/PDP-11/20 instruction subset. See
  `docs/PDP11-ORACLE.md`.
- `build_stage3a.py`: fixed-layout class-M builder for the four Stage 3A word
  manifests and explicit SIMH deposit scripts. It is intentionally not a
  general assembler.
- `build_stage3b.py`: fixed-layout class-M extension for Stage 3B control,
  call/frame, argument, return, and nested-call deposits; also not an assembler.
- `run_stage4a.py`: class-M automation of the already established native
  Stage 4A procedure on authoritative `machines/pdp7`. It transfers sources
  with terminal pacing, builds/runs as `shankao`, captures evidence, and checks
  output; rewind and I/O semantics execute on PDP-7, not in Python.
