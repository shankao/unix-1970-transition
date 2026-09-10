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

## Stable project hierarchy

Plan-level identifiers name known, meaningful capability boundaries. Items
inside a milestone are checkboxes, not necessarily a strict implementation
sequence: one implementation sweep may satisfy several of them, and smaller
debugging tasks remain beneath their existing checkbox. If evidence requires a
genuinely new plan-level boundary, this file must define and justify it before
implementation rather than inventing a new apparent stage afterward.

### Historical / bootstrap foundation

- [x] **Stage 0 — Machine reproducibility**
- [x] **Stage 1 — PDP-7 B characterization**
- [x] **Stage 2 — Independent KA11 verification oracle**
- [x] **Stage 3 — Standalone threaded-B PDP-11 execution**
  - [x] **Stage 3A — Runtime nucleus**
  - [x] **Stage 3B — Control, frames, calls, nesting**
- [x] **Stage 4 — PDP-7-hosted PDP-11 assembler bootstrap**
  - [x] **Stage 4A — B I/O / two-pass substrate**
  - [x] **Stage 4B — Scanner/parser/symbol/expression engine**
  - [x] **Stage 4C — KA11 encoder nucleus**

### Common migration research / contracts

- [x] **R1 — PDP-7 UNIX migration corpus**
- [x] **R2 — Bare KA11 machine contract**
- [x] **R3 — Core-only execution/RAM contract**
- [x] **R4 — Filesystem/kernel-structure contract**
- [x] **R5 — Repository-aware implementation inspection**

### Bootstrap / Ritchie-oriented track

- [ ] **B1 — Workload-driven as11 closure** (IN PROGRESS)
  - [x] **B1.1 — Native as11 -> exact KA11 execution path proven**
  - [x] **B1.2 — First workload-driven extension set proven**: `rti`,
    `trap`, `bit`, `bic`, and `bis`.
  - [ ] **B1.3 — Add further mnemonics/directives only when U/B workloads
    require them**
  - [ ] **B1.4 — Freeze the final as11 output/map/language contract** after
    real byte, data, syscall, and compiler workloads expose what is needed.
  - [ ] **B1.5 — Characterize capacity with realistic U and B workloads**
  - [ ] **B1.6 — Establish clean exhaustion/error behavior and the final
    bootstrap safety envelope**
- [ ] **B2 — PDP-7-hosted b11 cross-compiler**
  - [ ] **B2.0 — Freeze b11 provenance/source strategy and target-emission
    contract**
  - [ ] **B2.1 — Map characterized PDP-7 B semantics/emission vocabulary onto
    PDP-11 threaded-B operators**
  - [ ] **B2.2 — Produce readable as11 source for characterized B constructs**
  - [ ] **B2.3 — Cover selected-corpus constants, globals, autos, control,
    calls, returns, unary forms, and vector forms**
  - [ ] **B2.4 — Native PDP-7 deterministic compiler-output regression**
- [ ] **B3 — B -> b11 -> as11 -> PDP-11 integration**
  - [ ] **B3.1 — Close threaded-runtime operators required by selected
    compiled fixtures**
  - [ ] **B3.2 — Add only as11 capabilities forced by b11 output**
  - [ ] **B3.3 — Native PDP-7 B source -> b11 -> native as11**
  - [ ] **B3.4 — Execute exact PDP-7-produced words on PDP-11**
  - [ ] **B3.5 — Nontrivial end-to-end regression with no host target-code
    generation**
- [ ] **B4 — Paper-tape transport**
  - [x] **B4.0 — Freeze conservative paper-tape transport/loader contract**
  - [ ] **B4.1 — Produce exact tape bytes through the PDP-7 punch path**
  - [ ] **B4.2 — Load through the PDP-11 PTR/bootstrap path**
  - [ ] **B4.3 — Prove tape bytes -> memory identity**
  - [ ] **B4.4 — Replace modern deposit for one already-proven payload**
- [ ] **B5 — Across the Floor**
  - [ ] **B5.1 — Edit B source on PDP-7**
  - [ ] **B5.2 — Native b11 -> as11 -> paper-tape production**
  - [ ] **B5.3 — Carry the unchanged tape representation to PDP-11
    PTR/loader**
  - [ ] **B5.4 — Execute on PDP-11 and observe behavior corresponding to the
    source change**
  - [ ] **B5.5 — Repeat the complete workflow with no host-side target-code
    generation**
- [ ] **B6 — Small B calculator confidence probe** (OPTIONAL)
  - [ ] **B6.1 — Parser/stack/control-flow workload**
  - [ ] **B6.2 — Software-arithmetic workload**
  - [ ] **B6.3 — Complete reconstructed development/transport execution**
- [ ] **B7 — Historically constrained dc0** (high uncertainty; non-blocking)
  - [ ] **B7.0 — Historical feature/provenance research gate**
  - [ ] **B7.1 — Freeze minimal number representation, stack, parser, and
    evidenced command set**
  - [ ] **B7.2 — Implement the evidenced multiprecision arithmetic nucleus**
  - [ ] **B7.3 — Run dc0 through the reconstructed B/runtime path**
  - [ ] **B7.4 — Run through the complete paper-tape path**
  - [ ] **B7.5 — Preserve evidence and distinguish attested behavior from
    reconstruction**

This track is parallel. It is not a mandatory prerequisite chain for the UNIX
track. The Ritchie-oriented and Thompson-oriented names describe conceptual
emphasis, not exclusive authorship; the historical work was collaborative and
crossed these boundaries.

B1 receives requirements from real Unix and B workloads and closes only after
those workloads establish the needed language and its capacity/error envelope.
The Stage-4C static remainder is therefore evidence, not the final limit. B2.0
must record whether `b11` closely adapts the GPL restoration compiler or is a
new implementation of the behavioral contract, then construct an explicit
PDP-7 emission -> PDP-11 representation -> runtime operator -> `as11`
capability matrix before implementation.

B4 is independently actionable from the stable U1 payloads and does not wait
for B2/B3. U2 does not technically depend on it. B4 is nevertheless the
immediate next work because U1 transport acceptance is incomplete. B5,
dependent on B3 plus
B4, is the central historical
cross-development culmination. B6 is only an engineering confidence probe and
blocks nothing. B7 depends on its own research and sufficient B/runtime/tape
infrastructure; it is historically valuable but blocks neither Unix nor B5.

The dependency shape is:

```text
real U workloads ----+
                     +--> workload-forced as11 growth --> eventual B1 closure
real B workloads ----+

stable U1 payloads ------> B4 paper-tape work --> U1.7 --> U1 acceptance

B2 --> B3 --+
             +--> B5 Across the Floor
B4 ----------+
```

### UNIX / Thompson-oriented migration track

- [ ] **U1 — Bare PDP-11 machine substrate** (implementation proven;
  historical transport acceptance pending)
  - [x] **U1.1 — Stage-3 gold round trip**
  - [x] **U1.2 — KL11 polling input/output**
  - [x] **U1.3 — Low-core vectors + RTI**
  - [x] **U1.4 — Interrupt-driven KL11 console**
  - [x] **U1.5 — TRAP/syscall entry and return**
  - [x] **U1.6 — RAM storage primitive**
  - [ ] **U1.7 — Historical/mechanical-load acceptance**
- [ ] **U2 — Filesystem nucleus**
  - [ ] **U2.1 — RAM filesystem initialization**: inode bitmap, inode
    block, and root block.
  - [ ] **U2.2 — Inode/direct-block layer**: `iget`, `iput`, `pget`, and
    `itrunc`.
  - [ ] **U2.3 — Directory/name layer**: `dget`, `dput`, `namei`, `dslot`,
    and `icreat`.
  - [ ] **U2.4 — Descriptor/file-I/O layer**: descriptor allocation, `open`,
    `creat`, `close`, `read`, and `write`.
  - [ ] **U2.5 — Remaining core filesystem semantics**: `unlink`, `status`,
    and `ttyin`/`ttyout` special files.
- [ ] **U3 — Process/execution nucleus**
  - [ ] **U3.1 — Process record + user-image save/restore**
  - [ ] **U3.2 — PDP-7-shaped child-first fork**
  - [ ] **U3.3 — exit + resident/backed process selection**
  - [ ] **U3.4 — minimal smes + wakeup/blocking interaction**
  - [ ] **U3.5 — shell-controlled raw-image loader at 030000**: high-core
    argv and initial stack.
- [ ] **U4 — Minimal userland**
  - [ ] **U4.1 — cat**
  - [ ] **U4.2 — rm**
  - [ ] **U4.3 — stat**
  - [ ] **U4.4 — reduced streaming ls**
  - [ ] **U4.5 — sh**
- [ ] **U5 — Core-only UNIX integration**
  - [ ] **U5.1 — Initial RAM filesystem state created by PDP-11 code**
  - [ ] **U5.2 — 24 KB capacity validation**
  - [ ] **U5.3 — Core-only historical-transport acceptance demonstration**
- [ ] **U6 — RF11/RS11 transition**
  - [ ] **U6.0 — Focused RF11 / first-disk research gate**
  - [ ] **U6.1 — RF11/RS11 raw block-I/O diagnostic**
  - [ ] **U6.2 — Persistent filesystem backend**
  - [ ] **U6.3 — Disk-backed process storage**
  - [ ] **U6.4 — Full pathname traversal**
  - [ ] **U6.5 — exec + wait transition**
  - [ ] **U6.6 — Disk-backed integration**
- [ ] **U7 — First disk-backed PDP-11 UNIX acceptance**

U1.3 through U1.6 were completed as one checklist within the already-defined
U1 milestone. Technical dependencies determined coding order, but they were
not four successive project stages. This same checkbox rule governs later
milestones: incomplete items are refined beneath their existing identifier.
Several adjacent checkboxes may be authorized as one bounded implementation
slice when they are tightly coupled. Such a task still requires an explicit
upper scope boundary, stop condition, and validation; a checkbox need not
become a separate prompt or commit.

A parent R/B/U milestone is complete only when its separately documented
**Done when / observable outcome** passes, even if its implementation
checkboxes are checked. U1 was therefore reopened without invalidating
U1.1–U1.6: its missing historical transport acceptance is now U1.7.

## Transport provenance and acceptance policy

Code-generation provenance and transport provenance are independent. U1.1–U1.6
proved that PDP-7-hosted `as11` produced the exact KA11 words subsequently
verified and executed, but class-M SIMH deposits did not prove how those words
would historically reach the PDP-11.

Two test modes remain permanently legitimate:

- **Fast development transport:** native PDP-7 `as11` -> exact `i`/`x`/`w`
  words -> host parse/oracle/deposit -> PDP-11 execution. The host may
  coordinate and verify but must never encode, replace, repair, or silently
  alter target words. This remains the normal fast regression path and is not
  historical transport.
- **Historical acceptance transport:** PDP-7-hosted production -> paper-tape
  representation -> emulated PDP-11 reader -> PDP-11-executed bootstrap and
  loader -> identical target memory -> execution. The harness may automate
  switches, deposits of the tiny bootstrap, tape attachment, starts, console
  interaction, and verification.

The general paper-tape transfer from PDP-7 to PDP-11 is historically attested.
The exact late-1970 Bell Labs receiving loader and record format remain
unknown. Unless stronger Bell-specific evidence appears, B4 adopts the
contemporary DEC PDP-11 bootstrap plus Absolute Loader and fixed-address
absolute-binary mechanism as a **class-C conservative reconstruction**, not as
recovered Bell Labs practice. Contemporary documentation's approximately
fourteen-word bootstrap near the top of 24 KB is a plausible front-panel load;
large payloads are not.

The durable ergonomics rule is: **reconstruct historical mechanisms, not
historical operator tedium.** Authenticity requires that the PDP-11 execute the
reconstructed loader and consume tape through the reader, not that a person
manually toggle hundreds of words.

### U1.7 done when / observable outcome

U1.7 passes only when:

1. an already-proven substantial U1 payload is produced by native PDP-7
   `as11`;
2. its paper-tape representation is produced without host target-code
   generation;
3. PDP-11 bootstrap/loader code consumes the tape through the emulated reader;
4. loaded target memory is proven word-for-word identical to the native
   PDP-7-produced map; and
5. the loaded fixture reproduces its established U1 execution result.

The two current U1 fixtures total 342 native words. B4 implementation should
select the best substantial existing acceptance article rather than inventing
a trivial transport-only payload. B4.1–B4.4 supply the mechanism for U1.7;
only after it passes is the U1 parent complete and U2 again next.

The separate preservation view is:

```text
eras/
+-- stage-0, stage-1, stage-4a, stage-4b, stage-4c   existing PDP-7 eras
+-- pdp11-crossdev                                    DONE
+-- pdp11-core-unix                                   future; do not create yet
`-- pdp11-rf11-unix                                   future; do not create yet
```

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

#### Workload-driven `as11` closure gate (B1)

**Status: IN PROGRESS**

- **Objective:** integrate 4B and 4C into a genuine two-pass PDP-11 assembler
  written in B and running on the PDP-7. Final output, mnemonic/directive
  scope, and resource tests are driven by audited Unix and B workloads rather
  than completeness for its own sake. U1 already forced and validated `rti`,
  `trap`, `bit`, `bic`, and `bis` beyond the Stage-4C nucleus.
- **Gate:** repeatable assembly of representative multi-fragment sources on
  PDP-7, with the final textual address/word map, stable symbols, output,
  clean memory-exhaustion behavior, realistic bootstrap capacity, and a
  documented safety margin and final limits.

#### Stage-3 gold round-trip gate

**Status: COMPLETE**

- **Objective:** assemble the Stage 3 nested-call program with PDP-7 `as11`,
  verify its word map independently, then use class-M loading to run those
  exact PDP-7-produced words on the bare PDP-11.
- **Gate:** the verified map reproduces the known Stage 3 nested-call result
  with no host-created replacement words and no paper-tape claim.

The gold round trip is an important bootstrap regression and target-execution
proof, not a claim that the Stage 3 program is the UNIX migration workload.
The checked-in test-L fixture produces 110 words through native PDP-7 `as11`;
class-M code only parses and validates `i`/`x`/`w` records, and the PDP-11
executes those exact records to print `D`.

### B cross-compiler workstream — `b11`

**Status: NOT STARTED**

- **Objective:** reconstruct a PDP-7-hosted B-to-PDP-11 threaded-code compiler
  that feeds `as11` through readable assembly/representation.
- **Evidence basis:** cross-development is attested; Stage 1 is the source
  contract and Stage 3 the target ABI. Later compiler archaeology only
  supports comparison.
- **Major unknowns:** original source, structure, emitted syntax, and complete
  operator mapping are lost.
- **Initial gate (B2.0):** before implementation, freeze whether `b11` is a
  close adaptation of Robert Swierczek/DoctorWkt GPL restoration source or a
  new implementation of the recorded behavioral contract. Retain upstream
  GPL attribution for a close adaptation. Record a matrix from each selected
  PDP-7 B semantic/emission operation to its intended PDP-11 threaded form,
  existing or missing Stage-3 operator, and required `as11` capability.
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

**Status: IN PROGRESS — B4.0 COMPLETE; B4.1–B4.4 NEXT**

- **Objective:** replace deposits with `PDP-7 execution -> PTP -> exact tape
  image -> PDP-11 PTR -> loader -> execution`. Tape is transport/loading, not
  part of `b11` or `as11`.
- **Evidence basis:** physical transfer is directly attested; contemporary
  DEC loading documentation supplies the adopted conservative mechanism.
- **Major unknowns:** exact Bell Labs record and loader convention. DEC
  Absolute Binary must not be attributed to Bell Labs without evidence.
- **Dependencies:** a stable PDP-7-produced payload/map, PDP-7 PTP, and
  PDP-11 PTR. It need not wait for B2/B3 and is now actionable with U1 payloads.
- **B4.0 decision:** absent stronger Bell-specific evidence, use the
  contemporary DEC bootstrap plus Absolute Loader/absolute-binary mechanism
  as class C. This selects a reconstruction; it does not resolve the class-D
  Bell Labs format.
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

**Status: OPTIONAL / NOT STARTED**

- **Objective:** build a small standalone B calculator with console I/O,
  parser, stack/data structures, loops, calls, and `+ - * /`, using software
  arithmetic where needed.
- **Evidence basis:** a technical systems test, not a historical program.
- **Major unknowns:** runtime/library breadth, I/O robustness, arithmetic cost.
- **Dependencies:** sufficient standalone B runtime, cross tools, and the
  intended transfer path. It blocks neither B5, B7, nor Unix work.
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

**Status: RESEARCH AND U1.1–U1.6 IMPLEMENTATION COMPLETE; U1.7 ACCEPTANCE
PENDING**

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
- **Implementation gate result:** U1.1–U1.6 demonstrate exact native-`as11`
  execution, polling and interrupt-driven KL11 I/O, real low-core vector/RTI
  behavior, diagnostic TRAP entry/return, and the sixteen-block RAM primitive
  on the diskless 24 KB PDP-11 without importing later UNIX.
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

**Status: COMPLETE**

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

The inspection selected the bounded next implementation order: KL11 polling
input/output diagnostic, then low-core vectors and RTI, then interrupt-driven
console. The gold round trip was closed first so future PDP-11 machine words
have a proven PDP-7 `as11` integration path.

### KL11 polling input/output diagnostic

**Status: COMPLETE**

- **Objective:** prove two independent keyboard receives and transmitter
  writes through KL11 registers without interrupts.
- **Gate result:** native PDP-7 `as11` emitted 33 words / 19 instructions;
  class-M transport deposited them unchanged; controlled input `A`, then `B`,
  produced output `AB`, saved both bytes in RAM, and halted. The manual artifact
  is `artifacts/kl11-poll.simh`.
- **Scope:** bare-machine polling proof only. No vectors, interrupt enable,
  tty queue, syscall, or Unix code is present.

### U1 — Bare PDP-11 machine substrate

**Status: IMPLEMENTATION COMPLETE; PARENT REOPENED FOR U1.7 TRANSPORT
ACCEPTANCE**

The remaining U1 checklist was completed as one implementation sweep using two
focused native-`as11` fixtures. Real KL11 RX/TX interrupts enter vectors
060/064, preserve current-stack PC/PS frames, and return through `RTI`; a
diagnostic `TRAP 7` enters vector 034, decodes its call number, consumes one
inline argument, returns its result in R0, and resumes after that argument.
The RAM primitive maps sixteen 512-byte blocks, keeps blocks 0–1 out of the
common allocator, proves exhaustion and free/reuse, and copies a full block
without crossing its boundary. See `evidence/u1-substrate/`.

This is machine substrate, not a tty layer, syscall surface, process system,
or filesystem. U1.1–U1.6 remain complete. B4 paper-tape transport is next and
will supply U1.7; U2 remains unimplemented until that acceptance gap is closed.

When U2 begins, loaded PDP-11 code should itself clear and initialize the RAM
inode area, root directory, free maps, tty special entries, and test state. U2
does not require a host-generated/deposited 8 KB filesystem image. This is a
reconstruction design, not a recovered historical initialization procedure.

When U4 later populates real commands, paper tape is a natural input for their
bytes, but Bell Labs' exact RAM-filesystem population procedure is unknown.
Use the simplest reconstruction compatible with the established transport and
filesystem interfaces rather than asserting tape, programmatic creation, or a
mixture as historical fact.

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
  required bootstrap support; the accepted U1 substrate; and B4 historical
  transport for final acceptance.
- **Gate / observable outcome:** development may use fast deposits, but DONE
  requires PDP-7-produced system/command payloads loaded through paper tape and
  the real emulated loader into a 24 KB RAM-backed environment, followed by an
  interactive shell and the expected `ls`, `cat`, redirection, `stat`, and
  `rm` scenario within the memory budget.
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
first small PDP-11 form is now established for cross-developed runnable
diagnostics: an era-local clean machine config plus a native-`as11`-derived
deposit script. Layouts for future persistent RAM, tape, disk, or paired-machine
states remain deferred until those artifacts acquire concrete requirements.
