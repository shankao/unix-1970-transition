# UNIX 1970 Transition Reconstruction

## Across the Floor

This project reconstructs the 1970 transition from PDP-7 UNIX to the early
PDP-11/20 environment. “Across the Floor” recalls Dennis Ritchie’s description
of PDP-11 code being produced on the PDP-7, punched to paper tape, carried to
the new machine, and loaded there.

The project is not a claim that lost Bell Labs programs have been recovered.
It combines surviving artifacts, contemporary documentation, descendant
evidence, and conservative reconstruction into a system that fits the
surviving historical accounts. Every material component is identified as:

- **A — authentic surviving material**;
- **B — conservative reconstruction**;
- **C — contemporary or historically close substitute**;
- **D — missing, unknown, or unrecoverable**;
- **M — modern instrumentation or convenience**.

Class B, C, and M work is never represented as original Bell Labs source.

## What works now

Stages 0–3 and Stages 4A–4C are complete. The repository contains reproducible
PDP-7 and PDP-11 baselines, a characterized reconstructed PDP-7 B environment,
and a modern KA11 instruction oracle. Most importantly, the bare 24 KB
PDP-11/20 has executed a historically grounded direct-threaded B nucleus using:

```text
R3  threaded program counter
R4  B frame/display pointer
R5  B expression-stack pointer
```

The machine demonstrated constants, external and automatic access,
assignment, addition, true/false control, a loop, one- and two-argument calls,
void and value returns, and two simultaneously active frames. The observed
tests A through M produced the documented outputs in
[`docs/PDP11-B-RUNTIME.md`](docs/PDP11-B-RUNTIME.md). They used only the base
KA11 instruction set: no disk, UNIX, paper tape, KE11, EIS, or later CPU
hardware was involved. Their explicit SIMH memory deposits are class M test
instrumentation, not the final historical workflow.

## Where the project is going

The surviving/restored PDP-7 UNIX system is the principal source base for the
UNIX migration. Its provisional v1 kernel/command corpus, provenance layers,
and intended semantics are now frozen in
[`docs/UNIX-MIGRATION.md`](docs/UNIX-MIGRATION.md). The bare KA11 and
provisional core-only execution/RAM and filesystem/data-structure contracts
are complete. Repository-aware integration has now closed the Stage-3 gold
round trip: native PDP-7 `as11` output is transported without host encoding
and executes as Stage-3B test L on the PDP-11/20. The next implementation
KL11 polling input/output diagnostic is now complete: two independently
injected bytes were received, saved, and echoed by native-`as11`-produced
machine code. The next slice is the low-core vector/RTI framework, followed
by interrupt-driven console. The current
`as11` encoder remains a validated bootstrap nucleus, not the final
specification of the assembler.

Two related tracks then advance: the `as11`/threaded-B/`b11`/`dc` bootstrap
track and the migration of selected PDP-7 kernel and command responsibilities
to a minimal PDP-11 system. They converge on the destination machine. Cross
tools remain bootstrap scaffolding, and development should move onto the
PDP-11 once that becomes historically and technically justified.

The central standalone milestone is the complete “Across the Floor” loop:

```text
edit B source on PDP-7
    -> b11 -> as11 -> PDP-7 paper-tape punch
    -> unchanged tape image -> PDP-11 reader/loader
    -> standalone threaded-B execution
```

In parallel with those standalone milestones, the Unix-directed work targets
a single-console, core-only PDP-11/20 test system derived from selected PDP-7
responsibilities and using conservatively reconstructed RAM-backed storage.
The completion criterion for this repository is a reproducible first
disk-backed PDP-11 UNIX environment consistent with the surviving evidence for
the December 1970 RF11/RS11 disk transition.
Later 1971 development toward First Edition is outside the required scope and
may become a successor project.

## Historical boundary

The original 1970 B-written assembler, PDP-7-hosted PDP-11 B compiler, exact
diskless PDP-11 B runtime, early B `dc` source, Bell Labs tape encoding, and
core-only kernel source are not currently known to survive. Later manuals and
early/V1 archaeology constrain reconstructions but are not silently promoted
to 1970 originals. If the tape convention remains unknown, contemporary DEC
loading machinery may be used only as an explicit class C substitute—not as a
claim about Bell Labs practice.

## Start here

- [`docs/STATUS.md`](docs/STATUS.md) — authoritative current checkpoint and
  exact resume instructions.
- [`docs/PLAN.md`](docs/PLAN.md) — dependency-gated roadmap and completion
  criteria.
- [`docs/METHOD.md`](docs/METHOD.md) — evidence and provenance method.
- [`docs/STATE.md`](docs/STATE.md) — authoritative machine state.
- [`docs/SOURCES.md`](docs/SOURCES.md) — claim-level historical sources.
- [`docs/B-BASELINE.md`](docs/B-BASELINE.md) — PDP-7 B compiler/runtime
  contract.
- [`docs/PDP11-ORACLE.md`](docs/PDP11-ORACLE.md) — modern KA11 verification
  boundary.
- [`docs/PDP11-B-RUNTIME.md`](docs/PDP11-B-RUNTIME.md) — reconstructed runtime
  design and observed bare-machine results.
- [`docs/PDP11-MACHINE-CONTRACT.md`](docs/PDP11-MACHINE-CONTRACT.md) — KA11
  memory, trap, vector, console, and storage-abstraction boundary.
- [`docs/PDP11-EXECUTION-CONTRACT.md`](docs/PDP11-EXECUTION-CONTRACT.md) —
  provisional core-only memory partition, executable/ABI, process-backing,
  and RAM-storage contract.
- [`docs/PDP11-FILESYSTEM-CONTRACT.md`](docs/PDP11-FILESYSTEM-CONTRACT.md) —
  provisional inode, directory, descriptor, process-record, allocation, and
  resident-data contract.
- [`docs/UNIX-MIGRATION.md`](docs/UNIX-MIGRATION.md) — migration corpus,
  provenance refinements, and workload-driven forward architecture.

The repository layout separates historical/reconstructed target code in
`src/`, modern host tooling in `tools/`, regression tests in `tests/`, and
claim and execution evidence in `evidence/`. Source and reproducible build
steps are authoritative; generated images and listings are artifacts.
