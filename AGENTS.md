# Instructions for Coding Agents

This repository reconstructs a historically documented 1970 PDP-7 -> PDP-11 transition. Correct output is necessary but not sufficient; provenance and historical claims are part of correctness.

## Before changing code

1. Treat documentation at `HEAD` as authoritative. Read `README.md`,
   `docs/STATUS.md`, `docs/METHOD.md`, `docs/PLAN.md`, and `docs/STATE.md`.
2. Identify the current roadmap stage and its gate.
3. Check whether the requested change relies on a historical assertion. If so, verify/add the source in `docs/SOURCES.md` or `evidence/` before encoding the assertion in code.
4. Do not import third-party source until licensing/provenance is recorded.
5. Consume historical findings already recorded in `docs/SOURCES.md`, design
   documents, and `evidence/` instead of repeating broad research. New broad
   research is appropriate only for a genuinely unresolved question that
   affects the current gate.

## Required distinctions

Use these labels in design notes/commits when relevant:

- A authentic surviving material
- B conservative reconstruction
- C historically close substitute
- D unknown/unrecoverable
- M modern instrumentation/convenience

Never describe B/C/M material as original Bell Labs code.

## Development rules

- Every substantial stage, gate, or milestone commit must update
  `docs/STATUS.md` in the same commit so that `HEAD` describes the actual
  project state. If work fails or reveals a blocker, record that actual result
  in `STATUS.md`; never leave it describing only the intended state.
- Always use `machines/pdp7` as this project's PDP-7 development host. Treat
  `../PDP-7` as a read-only pre-transition/reference machine; never run project
  sessions against it or modify it.
- `machines/pdp7` is an evolving host: normal development and tests run there
  directly and may modify its filesystem. Inspect Git status and image hashes
  around meaningful work. Git is the recovery mechanism; do not revert
  legitimate project state merely to keep the image byte-identical.
- Do not commit a new PDP-7 filesystem image after every emulator session.
  Commit image versions only at meaningful, documented project milestones.
  A dirty image during active development is acceptable. Use a disposable copy
  only for a specifically identified destructive or high-risk experiment.
- Prefer a small verified implementation over a broad speculative one.
- Add automated regression vectors for reconstructed instruction encoders, runtime operators, tape formats, and compiler output.
- Isolate failures at boundaries; do not compensate by silently adding later hardware/software.
- The PDP-11 target remains 11/20, 24 KB, diskless, without KE11 until a recorded decision changes that.
- Modern tools may verify output, but the final historical demonstration must make the program bytes on the PDP-7 side and transfer them through the paper-tape path.
- Generated tape images/listings are artifacts; source + reproducible build steps are authoritative.
- When a historical uncertainty affects implementation, stop and write a short decision/evidence note rather than guessing.
- Stage 4 (`as11`) is the next gate. Do not skip to `b11`, tape transport,
  `dc`, or UNIX because a later stage appears more interesting.
- Keep `as11`, `b11`, and paper-tape transport as separate architectural
  layers unless a recorded evidence-backed decision changes that boundary.

## PDP-7 development account policy

- Use `shankao` by default for project development, tests, reconstruction work,
  and generated artifacts on the persistent PDP-7 host.
- Do not switch to historical accounts such as `dmr`, `ken`, or others merely
  to bypass ownership, linking, pathname, or permission restrictions.
- Where historically reasonable, copy required files into a `shankao`-owned
  project workspace and leave authentic/recovered originals unchanged.
- Do not casually edit, change ownership of, or replace hard-linked authentic
  files, especially shared historical files such as `op.s`.
- If historical software genuinely depends on another account's identity or
  environment, document the reason and expected effect before using it.
- Clearly distinguish authentic historical files, copied working files,
  reconstructed files, and generated build artifacts.

## Interaction with the operator

Minimize terminal back-and-forth. Before asking for commands on the historical machines, investigate source/tool behavior and prepare one guarded, meaningful operation where practical.

For PDP-7 discovery/debugging, keep one interactive SIMH session alive and
test native operations incrementally; do not assume later-UNIX pathname,
shell, filesystem, stdio, or process semantics. Reuse established session and
flow-controlled transfer methods. Add host automation only after the native
procedure is understood. Such automation remains class M instrumentation and
is never a semantic substitute for PDP-7 UNIX.

## Commits

Keep commits stage-scoped. Suggested prefixes:

- `docs:` planning/evidence/provenance
- `tools:` modern verification tooling
- `pdp7:` code that executes on PDP-7
- `pdp11:` code that executes on PDP-11
- `test:` regression/end-to-end fixtures
- `evidence:` source/claim updates

A commit that changes a historical assumption should update the corresponding evidence/decision document in the same commit.
