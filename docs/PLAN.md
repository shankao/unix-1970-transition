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

Completed stage numbers remain stable historical labels. The forward roadmap
is now organized as cooperating dependency tracks rather than treating the
cross-tool chain as the definition of UNIX. The surviving/restored PDP-7 UNIX
workload defines the migration target; `as11`, threaded B, `b11`, and tape are
bootstrap infrastructure. See [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md).

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

## Migration corpus definition

**Status: COMPLETE — provisional v1 workload frozen**

- **Objective:** inventory the selected local PDP-7 kernel and command sources,
  assign source-level provenance, map responsibilities and intended PDP-11
  semantics, record omissions, and derive the actual KA11 instruction and
  assembler-directive requirements.
- **Evidence basis:** surviving contemporary PDP-7 listing/source lineages,
  their restored working forms, and primary accounts of the migration.
- **Major unknowns:** detailed line-level restoration provenance and the lost
  1970 PDP-11 implementation remain unresolved.
- **Dependencies:** completed Stages 0–4C and the source/provenance method in
  [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md).
- **Gate result:** [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md) freezes selected
  responsibilities from `s1`–`s8`, explicitly defers `s9`, selects `sh`,
  `cat`, `ls`, `rm`, and `stat`, records layered provenance and core-only
  semantics, and derives provisional assembler requirements.
- **Provenance:** the specification is M documentation over layered A1/A2
  listing evidence and restored B/local C forms; future translated PDP-11 code
  will normally be project-wide class B.

This freeze selects work; it does not prove the exact December-1970 corpus or
port code. It now constrains final `as11` feature decisions and the core-only
UNIX implementation track.

## Bootstrap track — PDP-11 bootstrap substrate

### `as11` historical workstream

**Status: Stages 4A–4C COMPLETE; future work continues through named
gates**

- **Objective:** reconstruct the attested simple PDP-11 assembler in B and run
  it on `machines/pdp7` as `shankao`. It assembles PDP-11 code; it does not own
  the paper-tape protocol or define the PDP-11 UNIX target.
- **Evidence basis:** participant accounts attest the B-written assembler;
  Stage 3 provides the first verified encoder corpus, selected UNIX migration
  workloads drive later requirements, and Stage 2 independently checks words.
- **Major unknowns:** original source, exact language, directives, symbols,
  and object convention are lost.
- **Dependencies:** Stages 1–3 and the persistent PDP-7 host.
- **Gate:** PDP-7 `as11` reproduces the known Stage 3 words and can assemble
  the bootstrap-sufficient subset derived from selected migration workloads.
- **Provenance:** assembler B; oracle and host harness M.

The completed 4A–4C labels remain the historical record. Prospective work is
named rather than extended into a false numerical sequence. Each passing
PDP-7 development gate checkpoints the authoritative filesystem image and
useful native artifacts unless that gate explicitly made no PDP-7 state change.
The cross-tools are bootstrap scaffolding: each gate implements what is needed
to reach the next useful PDP-11 capability, not completeness for its own sake.
Stage 4C is also the first checkpoint expected to maintain a short native
`dd/shankao/readme` for someone exploring the machine from inside PDP-7 UNIX.

#### Stage 4A — PDP-7 B I/O substrate

**Status: COMPLETE**

- **Objective:** prove an ordinary PDP-7 B program can reread input reliably
  at mid-buffer, across refill, and after EOT/EOF, and can emit deterministic
  six-digit textual octal. Provide only the minimal B-callable rewind support
  required by a real two-pass tool.
- **Gate:** all rewind and textual-output cases execute under `shankao` in the
  authoritative PDP-7 UNIX/B environment; shared authentic `bl.s` remains
  unchanged and filesystem-image changes are inspected and explained.

#### Stage 4B — Assembler language and symbol engine

**Status: COMPLETE**

- **Objective:** define, tokenize, and parse the conservative early-UNIX
  assembly language and perform two-pass symbol and local-label resolution.
  Do not encode PDP-11 instructions in this gate.
- **Gate:** PDP-7 B tests demonstrate deterministic pass restart, tokenization,
  symbols, local labels, location accounting, and diagnostics over a fixed
  language corpus.
- **Capacity scope:** its standalone stress measurements characterize that
  implementation; they do not permanently require a larger later integrated
  executable to retain the identical maximum count.

#### Stage 4C — PDP-11 encoding engine

**Status: COMPLETE**

- **Objective:** add KA11 operands/instructions, extension words, branches,
  and raw-word emission to the established language/symbol engine.
- **Gate:** exhaustive fixed encodings produced by PDP-7 B agree with the
  independent Stage 2 oracle, including negative and range cases; Stage 4B
  language semantics remain available and the current Stage-3-shaped
  bootstrap workload fits ordinary B.
- **Scope:** the Stage-3-derived mnemonic set is a validated encoder nucleus
  and B-bootstrap test corpus, not the final historically derived assembler
  requirement.

#### Unix-driven `as11` completion gate

**Status: NOT STARTED**

- **Objective:** integrate 4B and 4C into a genuine two-pass PDP-11 assembler
  written in B and running on the PDP-7. Final output, mnemonic/directive
  scope, and resource tests are driven by the audited migration corpus rather
  than completeness for its own sake.
- **Gate:** repeatable assembly of representative multi-fragment sources on
  PDP-7, with the final textual address/word map, stable symbols, output,
  clean memory-exhaustion behavior, realistic bootstrap capacity, and a
  documented safety margin and final limits.

#### Stage-3 gold round-trip gate

**Status: NOT STARTED**

- **Objective:** assemble the Stage 3 nested-call program with PDP-7 `as11`,
  verify its word map independently, then use class-M loading to run those
  exact PDP-7-produced words on the bare PDP-11.
- **Gate:** the verified map reproduces the known Stage 3 nested-call result
  with no host-created replacement words and no paper-tape claim.

The gold round trip remains an important bootstrap regression and
target-execution proof; it is not a claim that the Stage 3 program is the UNIX
migration workload.

### B cross-compiler workstream — `b11`

**Status: NOT STARTED**

- **Objective:** reconstruct a PDP-7-hosted B-to-PDP-11 threaded-code compiler
  that feeds `as11` through readable assembly/representation.
- **Evidence basis:** cross-development is attested; Stage 1 is the source
  contract and Stage 3 the target ABI. Later compiler archaeology only
  supports comparison.
- **Major unknowns:** original source, structure, emitted syntax, and complete
  operator mapping are lost.
- **Dependencies:** the Stage 1/3 contracts and enough verified `as11`
  capability for the compiler's actual output.
- **Gate:** representative B constructs compiled on PDP-7 produce `as11`
  input and words compatible with the demonstrated runtime.
- **Provenance:** compiler B; descendant evidence B/C; verification M.

### B toolchain integration gate — modern loading

**Status: NOT STARTED**

- **Objective:** prove `B source -> b11 -> as11 -> PDP-11 words -> modern
  deposit -> bare PDP-11 execution` before introducing tape.
- **Evidence basis:** compiler/assembler architecture is historical; loading
  is explicitly diagnostic.
- **Major unknowns:** compiler-output/runtime-ABI integration.
- **Dependencies:** working `b11`, its required `as11` subset, and Stage 3
  runtime regressions.
- **Gate:** a nontrivial B program is compiled and assembled on the PDP-7 and
  runs on the PDP-11 using class-M loading.
- **Provenance:** tools/runtime B; deposits and coordination M.

### Paper-tape transport milestone

**Status: NOT STARTED**

- **Objective:** replace deposits with `PDP-7 execution -> PTP -> exact tape
  image -> PDP-11 PTR -> loader -> execution`. Tape is transport/loading, not
  part of `b11` or `as11`.
- **Evidence basis:** physical transfer is directly attested; contemporary
  DEC loading documentation supplies a possible fallback.
- **Major unknowns:** exact Bell Labs record and loader convention. DEC
  Absolute Binary must not be attributed to Bell Labs without evidence.
- **Dependencies:** a stable PDP-7-produced payload/map, a selected loader,
  PDP-7 PTP, and PDP-11 PTR. It need not wait for unrelated B or UNIX work.
- **Gate:** exact bytes produced through PDP-7 execution/PTP are attached
  unchanged to PTR, loaded, and executed. A host replacement tape fails it.
- **Provenance:** transfer A; exact format D; DEC fallback C if selected;
  host coordination M.

### Complete “Across the Floor” milestone

**Status: NOT STARTED**

- **Objective:** demonstrate `edit B on PDP-7 -> b11 -> as11 -> PTP -> tape
  -> PTR -> standalone runtime -> changed behavior` repeatably, without large
  manual memory dumps.
- **Evidence basis:** primary participant descriptions of the workflow.
- **Major unknowns:** robustness across all reconstructed boundaries.
- **Dependencies:** the required `b11`/`as11` path, standalone B runtime, and
  proven paper-tape transport—not the Unix migration track.
- **Gate:** editing PDP-7 source and repeating the unchanged-tape path changes
  observed PDP-11 behavior.
- **Provenance:** workflow A; lost tools/runtime B; loader fallback C;
  orchestration M.

This is the central reconstruction milestone and an independent success even
if later UNIX reconstruction proves infeasible.

## Bootstrap track — use the reconstructed B environment

### Small machine-word RPN calculator probe

**Status: NOT STARTED**

- **Objective:** build a small standalone B calculator with console I/O,
  parser, stack/data structures, loops, calls, and `+ - * /`, using software
  arithmetic where needed.
- **Evidence basis:** a technical systems test, not a historical program.
- **Major unknowns:** runtime/library breadth, I/O robustness, arithmetic cost.
- **Dependencies:** sufficient standalone B runtime, cross tools, and the
  intended transfer path.
- **Gate:** examples such as `2 3 + p -> 5` and `6 7 * p -> 42` work through
  the full PDP-7/tape/PDP-11 chain.
- **Provenance:** B/M project test, not claimed original.

### Historically constrained standalone `dc0`

**Status: NOT STARTED**

- **Objective:** incrementally reconstruct a conservative early standalone B
  `dc`: parser, stack, output, number representation, multi-precision
  arithmetic, and only evidenced commands.
- **Evidence basis:** B `dc` and early multi-precision PDP-11 execution are
  attested; exact source and feature set are lost. Later V1 is comparison.
- **Major unknowns:** representation, commands, implementation, diskless
  behavior.
- **Dependencies:** focused feature research and the B/runtime/tool subset its
  evidenced behavior actually requires. The calculator is a useful confidence
  probe, not a historical dependency of UNIX or necessarily of `dc0`.
- **Gate:** documented behavior/provenance matrix and useful multi-precision
  execution on bare PDP-11 through the full development/transfer path.
- **Provenance:** B constrained by A; inference and later evidence separated.

## UNIX migration track — PDP-7 responsibilities on the PDP-11

This track is derived from the migration corpus rather than from V1 source.
It may advance alongside bootstrap work when dependencies permit, but no
translation begins before the corpus-definition gate. The two tracks converge
when selected PDP-7 responsibilities run on the PDP-11.

### Bare PDP-11/20 machine substrate

**Status: MACHINE-LAYER RESEARCH COMPLETE; IMPLEMENTATION NOT STARTED**

- **Objective:** establish only the machine services required by the selected
  core-only workload: vectors, stack, console, trap/syscall entry, and a
  RAM-backed block or storage layer.
- **Evidence basis:** KA11/console documentation, primary accounts, and the
  audited interfaces of the selected PDP-7 system.
- **Major unknowns:** exact diskless-1970 entry paths, active-user size, memory
  allocation, and RAM-storage geometry remain reconstruction choices.
- **Dependencies:** migration-corpus definition and independently verified
  encoding/build support for each selected fragment.
- **Research gate result:**
  [`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md) documents the 24 KB
  layout, absence of hardware user/kernel modes, vectors, trap/syscall entry
  and return implications, processor stack/state, KL11
  registers/vectors/interrupt behavior, minimum initialization, and
  conservative RAM user/backing-store organization, with uncertainties
  explicit.
- **Later implementation gate:** each selected substrate interface is
  demonstrated on the diskless 24 KB PDP-11 without importing later UNIX.
- **Provenance:** primarily B, with A documentation and M verification.

### Core-only execution and RAM-layout contract

**Status: RESEARCH COMPLETE; PROVISIONAL CONTRACT V1 FROZEN; IMPLEMENTATION NOT STARTED**

- **Objective:** turn the physical KA11 contract and provisional migration
  corpus into a feasible, still non-implemented execution/memory design.
- **Evidence basis:** the completed machine contract, provisional v1 command
  corpus, approximate historical 12 KB system envelope, and PDP-7 process and
  filesystem semantics.
- **Questions resolved provisionally:** executable image and load address;
  active-user and stack budgets; manual command loading; compact process
  save/restore; syscall ABI shape; available RAM backing; direct-block
  sufficiency; RAM block geometry. Exact call numbers, translated sizes, and
  structure encodings remain unresolved.
- **Dependencies:** completed corpus and bare KA11 machine-layer research.
- **Gate result:**
  [`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md) freezes a
  conservative 12/4/8 KB system/user/RAM partition, raw fixed-address command
  images, shell-controlled loading, a PDP-7-shaped symbolic TRAP ABI,
  child-first cooperative residency, compact process backing, and provisional
  512-byte RAM blocks. Exact historical boundaries and syscall numbers remain
  unknown, and all translated sizes remain empirical gates.
- **Provenance:** historical constraints A; PDP-7 predecessor and descendant
  evidence explicitly separated; design choices B; calculations M.

### Core-only filesystem and kernel data-structure contract

**Status: RESEARCH COMPLETE; PROVISIONAL CONTRACT V1 FROZEN; IMPLEMENTATION NOT STARTED**

- **Objective:** derive the smallest filesystem, process, and resident kernel
  structures needed by the frozen corpus inside the provisional execution/RAM
  budget.
- **Evidence basis:** selected PDP-7 `s2`/`s4`/`s5`/`s6`/`s8`
  responsibilities first; First Edition layouts only as descendant evidence.
- **Questions resolved provisionally:** inode/direct-address and directory
  layouts; console-special semantics; table limits; process-record envelope;
  common RAM-block allocation; compact `status`; resident-data estimate.
  Exact image assignments, structure offsets, queue size, translated sizes,
  and filesystem/process capacity remain empirical or implementation choices.
- **Dependencies:** completed migration, KA11-machine, and execution/RAM
  contracts.
- **Gate result:**
  [`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md) freezes ten
  copied per-process descriptors, one current inode, a 12-word inode, 10-byte
  directory entry, compact 13-word `status`, two 64-word process records,
  sixteen inodes, shared block/inode bitmaps, one block buffer, and direct-only
  4 KB files. It records under 1 KB of obvious mutable resident data and the
  capacity invariant without claiming the kernel or initial image fits yet.
- **Provenance:** surviving PDP-7 evidence A1/B; adaptations B; descendant
  comparisons clearly labelled; calculations M.

### Repository-aware first implementation slice

**Status: NEXT — INSPECTION/PLANNING ONLY**

- **Objective:** inspect the actual repository and turn the three completed
  contracts into the smallest evidence-backed implementation plan.
- **Required inspection:** current Stage-4C syntax/features and oracle; Stage-3
  load/execution harness; existing artifacts; dependency order among vectors,
  traps, KL11 polling/interrupts, RAM/block abstraction, filesystem, process
  control, and commands; tests; first meaningful PDP-11 snapshot point.
- **Gate:** a repository-specific plan identifies the first target and its
  bounded tests. Coding requires separate explicit authorization.
- **Dependencies:** completed corpus, machine, execution/RAM, and
  filesystem/data-structure contracts.

## UNIX migration milestone — core-only PDP-11 UNIX

### Core-only / RAM-filesystem PDP-11 UNIX milestone

**Status: NOT STARTED — VERY HIGH RISK**

- **Objective:** reconstruct a single-console pre-disk 24 KB test system from
  the selected PDP-7 kernel responsibilities and tiny command corpus, with a
  small active user area, process creation/execution, basic file I/O, and
  RAM-backed storage. It is not “V1 without a disk.”
- **Evidence basis:** contemporary accounts constrain the core-only period
  and rough partition (about 12 KB OS, tiny user area, remainder RAM
  filesystem); PDP-7 UNIX is predecessor evidence and earliest PDP-11 UNIX is
  descendant evidence.
- **Major unknowns:** exact kernel, layout, interfaces, commands, filesystem.
- **Dependencies:** the corpus-definition, machine, execution/RAM, and
  filesystem/data-structure contracts; an approved implementation ordering;
  required bootstrap support; and the implemented bare-machine substrate.
- **Gate:** reproducible core-only system mapped through the predecessor /
  accounts / descendant evidence triangle with every inference exposed.
- **Provenance:** mainly B, constrained by A and B/C; unknowns D; harness M.

Failure here does not invalidate the completed stages or independent bootstrap
milestones.

## UNIX migration milestone — December 1970 disk transition

### RF11/RS11 arrival and first disk-backed UNIX milestone

**Status: NOT STARTED**

- **Objective:** model the disk arrival and migrate the core-only system to a
  working disk-backed PDP-11 UNIX environment representing December 1970.
- **Evidence basis:** accounts, DEC hardware, and early `rf0` descendant
  documentation support the present hypothesis: RF11 plus one RS11,
  256K 16-bit words (512 KB; 1024 blocks of 256 words).
- **Major unknowns:** exact physical unit, migration, source, and first-disk
  behavior.
- **Dependencies:** a demonstrated core-only system and a focused
  hardware/filesystem evidence gate.
- **Gate:** reproducible first disk-backed PDP-11 UNIX consistent with the
  December-1970 evidence and the focused findings on early memory, residency,
  pathname traversal, and introduction of `exec` and `wait`.
- **Provenance:** hardware identification is strong reconstruction evidence,
  not proof; reconstructed system B; authentic documentation A; harness M.

**This disk-backed-system gate is the completion criterion for this
repository.** Later 1971 work and the approach to First Edition are outside
required scope.

## Development ratchet and later expansion

Once the PDP-11 can support useful native development, subsequent work should
move there where historically and technically justified. The PDP-7 remains a
preserved fallback and historical development state, not the required forever
host for a comprehensive PDP-11 toolchain. Broader editor, text-processing,
and other 1971 expansion is outside this repository's completion criteria.

## Risk and confidence

| Boundary | Technical risk | Historical uncertainty |
| --- | --- | --- |
| migration-corpus definition | low | medium–high provenance work |
| `as11` | medium | medium |
| `b11` | medium | medium–high |
| toolchain integration | low–medium | low |
| paper-tape transport | low–medium | exact Bell encoding unknown |
| small B calculator | medium | low; not a reconstruction |
| `dc0` | medium | high |
| bare PDP-11 substrate | high | high |
| core-only UNIX | very high | very high |
| RF11/RS11 migration | high | medium |
| first disk-backed UNIX | high | medium–high |

Project value is incremental: Stage 3 already proves a grounded execution
architecture; the “Across the Floor” loop is a major standalone success; and
`dc0` is another independent milestone. The core-only system is a high-risk
extension, not a condition for those earlier results to count.

## Durable deliverables

At every gate preserve source, tests, claim notes, reproducible machine state,
and artifact metadata. Generated tapes/listings are artifacts; source plus
reproducible build steps are authoritative. Informative failures remain
evidence rather than being erased by later success.

Selected PDP-7 checkpoints that meaningfully expose a distinct development
state are also materialized as ordinary exact images under `eras/`. This
experiential layer supplements rather than replaces per-gate checkpoints. A
layout for future PDP-11 RAM/tape/disk or paired-machine eras remains deferred
until those artifacts acquire concrete operating requirements.
