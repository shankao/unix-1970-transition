# Instructions for Coding Agents

This repository reconstructs a historically documented 1970 PDP-7 -> PDP-11 transition. Correct output is necessary but not sufficient; provenance and historical claims are part of correctness.

## Before changing code

1. Treat documentation at `HEAD` as authoritative. Read `README.md`,
   `docs/STATUS.md`, `docs/METHOD.md`, `docs/PLAN.md`, `docs/STATE.md`, and
   `docs/UNIX-MIGRATION.md`. For PDP-11 machine or migration work, also read
   `docs/PDP11-MACHINE-CONTRACT.md` and
   `docs/PDP11-EXECUTION-CONTRACT.md` and
   `docs/PDP11-FILESYSTEM-CONTRACT.md`. The migration documents define the
   PDP-7-derived target and provenance discipline, the core-only PDP-11 UNIX
   concept, the bootstrap/UNIX-track relationship, and the rule that real
   workloads drive machine and assembler requirements.
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
- A dirty PDP-7 image is acceptable while a substage is in progress. Each
  successfully completed PDP-7 development substage/gate normally checkpoints
  the authoritative filesystem image in Git, together with its hash and useful
  native sources, build products, inputs, and results. Remove only clearly
  accidental debris. Use a disposable copy only for a specifically identified
  destructive or high-risk experiment.
- Development checkpoints and experiential snapshots are distinct. Every
  passing PDP-7 development gate normally checkpoints `machines/pdp7`; selected
  states that meaningfully show the development journey are also preserved as
  ordinary physical files under `eras/`. Do not invent an era manager. The
  first established PDP-11 form is the small `pdp11-crossdev` config plus
  runnable diagnostic; do not extrapolate it into future RAM/tape/disk layouts.
- While PDP-7-only state is sufficient, a selected experiential era is a
  self-contained directory containing `README.md`, `boot.rim`, `pdp7.fs`, and
  `pdp7.simh`, bootable from that directory without a wrapper. Small duplicated
  bootstrap/configuration files are preferable to premature management tooling.
- Beginning with the next successful PDP-7 development checkpoint (Stage 4C),
  maintain a concise native `dd/shankao/readme` describing what works and what
  does not yet exist. Update it as part of normal native development; never
  alter an older snapshot retroactively to insert it.
- Prefer a small verified implementation over a broad speculative one.
- Keep repository Python runners non-executable and invoke them explicitly as
  `python3 tools/<runner>.py`; do not add executable bits merely for
  convenience unless a specific existing convention documents the exception.
- Add automated regression vectors for reconstructed instruction encoders, runtime operators, tape formats, and compiler output.
- Isolate failures at boundaries; do not compensate by silently adding later hardware/software.
- The PDP-11 target remains 11/20, 24 KB, diskless, without KE11 until a recorded decision changes that.
- Modern tools may verify output, but the final historical demonstration must make the program bytes on the PDP-7 side and transfer them through the paper-tape path.
- Generated tape images/listings are artifacts; source + reproducible build steps are authoritative.
- When a historical uncertainty affects implementation, stop and write a short decision/evidence note rather than guessing.
- Stages 4A–4C, the provisional v1 migration-corpus audit, the bare KA11
  machine-layer contract, provisional execution/RAM contract v1, and
  provisional filesystem/data-structure contract v1 are complete. The
  Stage-3 gold round trip and KL11 polling diagnostic are also complete. The
  next bounded gate is low-core vector entry and RTI return. Do not implement
  structures,
  start kernel/command ports, or skip to `b11`, tape transport, `dc`, or later
  UNIX work before that contract is defined and passed.
- Keep `as11`, `b11`, and paper-tape transport as separate architectural
  layers unless a recorded evidence-backed decision changes that boundary.
- Treat PDP-7 cross-development tools as bootstrap scaffolding: implement the
  minimum evidenced capability needed to reach the next useful PDP-11 state,
  not features merely for tool completeness.
- Derive further assembler and cross-tool requirements from selected,
  provenance-recorded PDP-7 UNIX migration workloads. Stage 4C's Stage-3
  instruction inventory is a verified encoder nucleus, not the final `as11`
  catalogue. See `docs/UNIX-MIGRATION.md`.

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

Before depending on an unfamiliar PDP-7 command—especially in automation—
inspect its checked-in recovered source, project documentation, or existing
evidence for its real invocation and important semantics. Where practical,
confirm that understanding with one minimal interactive native operation, then
automate the observed procedure. Do not infer a later-Unix interface merely
from a familiar command name; see `docs/PDP7-TOOLS.md`.

Native PDP-7 work being slow is acceptable and sometimes informative. Improve
orchestration—persistent sessions, avoiding redundant transfers, and automating
known procedures—but do not move compilation, assembly, execution, or required
filesystem work to a modern host solely for speed.

The recovered PDP-7 `ed` is not later Unix `ed`: invoke `ed`, then use `r name`
to load an existing file; `ed name` does not load it. For native edits, use
only the source-verified commands and syntax in `docs/PDP7-TOOLS.md`. Send one
complete physical command line at a time and wait for its result. Locate and
print the target before changing it, print and verify it afterward, then write
explicitly and send `q` separately. The terminal uses `#` to erase one
character and `@` to kill the input line; do not assume Backspace/Delete.
Prefer a known-good retransmission over a long or ambiguous edit sequence, and
automate only a sequence first proven this way.

Stage 4A observed that the configured terminal/editor transfer path lowercased
alphabetic characters. This is not evidence that PDP-7 filenames, B, or its
scanner are lowercase-only. Preserve exact case in tests and comparisons, use
established lowercase historical names rather than invented uppercase variants,
and verify the transfer path before relying on case-sensitive Stage 4 input.

## Commits

Keep commits stage-scoped. Suggested prefixes:

- `docs:` planning/evidence/provenance
- `tools:` modern verification tooling
- `pdp7:` code that executes on PDP-7
- `pdp11:` code that executes on PDP-11
- `test:` regression/end-to-end fixtures
- `evidence:` source/claim updates

A commit that changes a historical assumption should update the corresponding evidence/decision document in the same commit.
