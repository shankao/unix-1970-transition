# Dependency-Gated Project Plan

## Purpose and endpoint

This roadmap reconstructs the 1970 path from late PDP-7 UNIX, through the
diskless PDP-11/20 cross-development period, to a first disk-backed PDP-11
UNIX environment consistent with the December 1970 disk arrival. It does not
require reconstruction of the rest of 1971 or First Edition; that belongs in
a possible successor project.

Stages advance only when their dependency boundary has passed. Evidence
confidence and technical feasibility are recorded separately. See
[`METHOD.md`](METHOD.md) for A/B/C/D/M policy and [`STATUS.md`](STATUS.md) for
the authoritative checkpoint.

## Phase I — Establish and prove the execution model

### Stage 0 — Machine reproducibility

**Status: COMPLETE.** Imported the persistent PDP-7 project host, retained the
sibling reference machine, and recorded deterministic PDP-7/PDP-11 static
state. Gate: machines can be recreated without chat history. See
[`STATE.md`](STATE.md).

### Stage 1 — PDP-7 B characterization

**Status: COMPLETE.** Characterized the reconstructed PDP-7 B compiler and
surviving/restored runtime through inventory and native probes. Gate: the
B-source-to-threaded-runtime contract is documented in
[`B-BASELINE.md`](B-BASELINE.md).

### Stage 2 — Modern KA11 verification oracle

**Status: COMPLETE.** Built the independent class-M encoder/decoder. Gate:
fixed DEC vectors, extensions, branches, bytes, and bootstrap decode pass;
later EIS is rejected. See [`PDP11-ORACLE.md`](PDP11-ORACLE.md).

### Stage 3 — Standalone threaded-B execution

**Status: COMPLETE (3A and 3B).** Reconstructed and ran the R3/R4/R5 nucleus,
then control, frames, arguments, calls, and returns on the bare PDP-11/20.
Gate: A–M machine tests, including loop and nested frames, pass using only
KA11 instructions and no disk, UNIX, tape, or KE11. The exact 1970 source is
lost; this is class B. See [`PDP11-B-RUNTIME.md`](PDP11-B-RUNTIME.md).

## Phase II — Reconstruct the PDP-7 → PDP-11 toolchain

### Stage 4 — `as11`

**Status: NEXT — NOT STARTED**

- **Objective:** reconstruct the attested simple PDP-11 assembler in B and run
  it on `machines/pdp7` as `shankao`. It assembles PDP-11 code; it does not own
  the paper-tape protocol.
- **Evidence basis:** participant accounts attest the B-written assembler;
  Stage 3 bounds its required output and Stage 2 independently checks words.
- **Major unknowns:** original source, exact language, directives, symbols,
  and object convention are lost.
- **Dependencies:** Stages 1–3 and the persistent PDP-7 host.
- **Gate:** PDP-7 `as11` reproduces known Stage 3 words byte-for-byte, or
  semantically identically where layout differences are intentional.
- **Provenance:** assembler B; oracle and host harness M.

### Stage 5 — `b11`

**Status: NOT STARTED**

- **Objective:** reconstruct a PDP-7-hosted B-to-PDP-11 threaded-code compiler
  that feeds `as11` through readable assembly/representation.
- **Evidence basis:** cross-development is attested; Stage 1 is the source
  contract and Stage 3 the target ABI. Later compiler archaeology only
  supports comparison.
- **Major unknowns:** original source, structure, emitted syntax, and complete
  operator mapping are lost.
- **Dependencies:** Stage 4 and the Stage 1/3 contracts.
- **Gate:** representative B constructs compiled on PDP-7 produce `as11`
  input and words compatible with the demonstrated runtime.
- **Provenance:** compiler B; descendant evidence B/C; verification M.

### Stage 6 — Toolchain integration with modern loading

**Status: NOT STARTED**

- **Objective:** prove `B source -> b11 -> as11 -> PDP-11 words -> modern
  deposit -> bare PDP-11 execution` before introducing tape.
- **Evidence basis:** compiler/assembler architecture is historical; loading
  is explicitly diagnostic.
- **Major unknowns:** compiler-output/runtime-ABI integration.
- **Dependencies:** Stages 4–5 and Stage 3 regressions.
- **Gate:** a nontrivial B program is compiled and assembled on the PDP-7 and
  runs on the PDP-11 using class-M loading.
- **Provenance:** tools/runtime B; deposits and coordination M.

### Stage 7 — Real paper-tape transport

**Status: NOT STARTED**

- **Objective:** replace deposits with `PDP-7 execution -> PTP -> exact tape
  image -> PDP-11 PTR -> loader -> execution`. Tape is transport/loading, not
  part of `b11` or `as11`.
- **Evidence basis:** physical transfer is directly attested; contemporary
  DEC loading documentation supplies a possible fallback.
- **Major unknowns:** exact Bell Labs record and loader convention. DEC
  Absolute Binary must not be attributed to Bell Labs without evidence.
- **Dependencies:** Stage 6, PDP-7 PTP, and PDP-11 PTR.
- **Gate:** exact bytes produced through PDP-7 execution/PTP are attached
  unchanged to PTR, loaded, and executed. A host replacement tape fails it.
- **Provenance:** transfer A; exact format D; DEC fallback C if selected;
  host coordination M.

### Stage 8 — Complete “Across the Floor” loop

**Status: NOT STARTED**

- **Objective:** demonstrate `edit B on PDP-7 -> b11 -> as11 -> PTP -> tape
  -> PTR -> standalone runtime -> changed behavior` repeatably, without large
  manual memory dumps.
- **Evidence basis:** primary participant descriptions of the workflow.
- **Major unknowns:** robustness across all reconstructed boundaries.
- **Dependencies:** Stages 0–7.
- **Gate:** editing PDP-7 source and repeating the unchanged-tape path changes
  observed PDP-11 behavior.
- **Provenance:** workflow A; lost tools/runtime B; loader fallback C;
  orchestration M.

This is the central reconstruction milestone and an independent success even
if later UNIX reconstruction proves infeasible.

## Phase III — Use the reconstructed B environment

### Stage 9 — Small machine-word RPN calculator

**Status: NOT STARTED**

- **Objective:** build a small standalone B calculator with console I/O,
  parser, stack/data structures, loops, calls, and `+ - * /`, using software
  arithmetic where needed.
- **Evidence basis:** a technical systems test, not a historical program.
- **Major unknowns:** runtime/library breadth, I/O robustness, arithmetic cost.
- **Dependencies:** Stage 8.
- **Gate:** examples such as `2 3 + p -> 5` and `6 7 * p -> 42` work through
  the full PDP-7/tape/PDP-11 chain.
- **Provenance:** B/M project test, not claimed original.

### Stage 10 — `dc0`

**Status: NOT STARTED**

- **Objective:** incrementally reconstruct a conservative early standalone B
  `dc`: parser, stack, output, number representation, multi-precision
  arithmetic, and only evidenced commands.
- **Evidence basis:** B `dc` and early multi-precision PDP-11 execution are
  attested; exact source and feature set are lost. Later V1 is comparison.
- **Major unknowns:** representation, commands, implementation, diskless
  behavior.
- **Dependencies:** Stage 9 and focused feature research.
- **Gate:** documented behavior/provenance matrix and useful multi-precision
  execution on bare PDP-11 through the full development/transfer path.
- **Provenance:** B constrained by A; inference and later evidence separated.

## Phase IV — Diskless UNIX

### Stage 11 — Core-only / RAM-filesystem UNIX

**Status: NOT STARTED — VERY HIGH RISK**

- **Objective:** reconstruct the pre-disk 24 KB system with an in-memory
  filesystem as a separate subproject—not “V1 without a disk.”
- **Evidence basis:** contemporary accounts constrain the core-only period
  and rough partition (about 12 KB OS, tiny user area, remainder RAM
  filesystem); PDP-7 UNIX is predecessor evidence and earliest PDP-11 UNIX is
  descendant evidence.
- **Major unknowns:** exact kernel, layout, interfaces, commands, filesystem.
- **Dependencies:** standalone development path and dedicated evidence audit.
- **Gate:** reproducible core-only system mapped through the predecessor /
  accounts / descendant evidence triangle with every inference exposed.
- **Provenance:** mainly B, constrained by A and B/C; unknowns D; harness M.

Failure here does not invalidate Stages 0–10.

## Phase V — December 1970 disk transition

### Stage 12 — RF11/RS11 arrival and first disk-backed UNIX

**Status: NOT STARTED**

- **Objective:** model the disk arrival and migrate the core-only system to a
  working disk-backed PDP-11 UNIX environment representing December 1970.
- **Evidence basis:** accounts, DEC hardware, and early `rf0` descendant
  documentation support the present hypothesis: RF11 plus one RS11,
  256K 16-bit words (512 KB; 1024 blocks of 256 words).
- **Major unknowns:** exact physical unit, migration, source, and first-disk
  behavior.
- **Dependencies:** Stage 11 and a focused hardware/filesystem evidence gate.
- **Gate:** reproducible first disk-backed PDP-11 UNIX consistent with the
  December-1970 evidence and supported early memory, residency, pathname,
  `exec`, and `wait` constraints.
- **Provenance:** hardware identification is strong reconstruction evidence,
  not proof; reconstructed system B; authentic documentation A; harness M.

**This Stage 12 gate is the completion criterion for this repository.** Later
1971 work and the approach to First Edition are outside required scope.

## Risk and confidence

| Boundary | Technical risk | Historical uncertainty |
| --- | --- | --- |
| `as11` | medium | medium |
| `b11` | medium | medium–high |
| toolchain integration | low–medium | low |
| paper-tape transport | low–medium | exact Bell encoding unknown |
| small B calculator | medium | low; not a reconstruction |
| `dc0` | medium | high |
| core-only UNIX | very high | very high |
| RF11/RS11 migration | high | medium |
| first disk-backed UNIX | high | medium–high |

Project value is incremental: Stage 3 already proves a grounded execution
architecture; Stage 8 is a major standalone success; and `dc0` is another
independent milestone. The core-only system is a high-risk extension, not a
condition for those earlier results to count.

## Durable deliverables

At every gate preserve source, tests, claim notes, reproducible machine state,
and artifact metadata. Generated tapes/listings are artifacts; source plus
reproducible build steps are authoritative. Informative failures remain
evidence rather than being erased by later success.
