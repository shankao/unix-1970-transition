# Instructions for Coding Agents

This repository reconstructs a historically documented 1970 PDP-7 -> PDP-11 transition. Correct output is necessary but not sufficient; provenance and historical claims are part of correctness.

## Before changing code

1. Read `README.md`, `docs/METHOD.md`, `docs/PLAN.md`, and `docs/STATE.md`.
2. Identify the current roadmap stage and its gate.
3. Check whether the requested change relies on a historical assertion. If so, verify/add the source in `docs/SOURCES.md` or `evidence/` before encoding the assertion in code.
4. Do not import third-party source until licensing/provenance is recorded.

## Required distinctions

Use these labels in design notes/commits when relevant:

- A authentic surviving material
- B conservative reconstruction
- C historically close substitute
- D unknown/unrecoverable
- M modern instrumentation/convenience

Never describe B/C/M material as original Bell Labs code.

## Development rules

- Always use `machines/pdp7` as this project's PDP-7 development host. Treat
  `../PDP-7` as a read-only pre-transition/reference machine; never run project
  sessions against it or modify it.
- Do not commit a new PDP-7 filesystem image after every emulator session.
  Commit image versions only at meaningful, documented project milestones.
- Prefer a small verified implementation over a broad speculative one.
- Add automated regression vectors for reconstructed instruction encoders, runtime operators, tape formats, and compiler output.
- Isolate failures at boundaries; do not compensate by silently adding later hardware/software.
- The PDP-11 target remains 11/20, 24 KB, diskless, without KE11 until a recorded decision changes that.
- Modern tools may verify output, but the final historical demonstration must make the program bytes on the PDP-7 side and transfer them through the paper-tape path.
- Generated tape images/listings are artifacts; source + reproducible build steps are authoritative.
- When a historical uncertainty affects implementation, stop and write a short decision/evidence note rather than guessing.

## Interaction with the operator

Minimize terminal back-and-forth. Before asking for commands on the historical machines, investigate source/tool behavior and prepare one guarded, meaningful operation where practical.

## Commits

Keep commits stage-scoped. Suggested prefixes:

- `docs:` planning/evidence/provenance
- `tools:` modern verification tooling
- `pdp7:` code that executes on PDP-7
- `pdp11:` code that executes on PDP-11
- `test:` regression/end-to-end fixtures
- `evidence:` source/claim updates

A commit that changes a historical assumption should update the corresponding evidence/decision document in the same commit.
