# Project Status

This is the authoritative handover checkpoint at HEAD. Use
[`PLAN.md`](PLAN.md) for gates, [`METHOD.md`](METHOD.md) for evidence policy,
[`STATE.md`](STATE.md) for machine details, and [`SOURCES.md`](SOURCES.md) and
[`DECISIONS.md`](DECISIONS.md) for claims and durable choices.

## Project and historical point

This repository reconstructs the 1970 transition from late PDP-7 UNIX to the
early PDP-11/20 environment. Surviving material is preferred; missing pieces
are reconstructed conservatively; contemporary substitutes are used only
when necessary; and every category is stated. Reconstructed programs are not
claimed to be the exact lost Bell Labs sources.

The demonstrated point is still the diskless late-1970 PDP-11/20, now with a
working reconstructed standalone threaded-B execution model and a PDP-7-hosted
KA11 encoder nucleus. The surviving/restored PDP-7 UNIX system is now the
principal source base for defining what migrates next. The repository’s
eventual boundary is the first disk-backed PDP-11 UNIX environment consistent
with the December 1970 disk arrival—not the rest of 1971 or First Edition.

## Current stage

```text
Stage 0  COMPLETE
Stage 1  COMPLETE
Stage 2  COMPLETE
Stage 3  COMPLETE (3A and 3B)
Stage 4A COMPLETE
Stage 4B COMPLETE
Stage 4C COMPLETE
Migration corpus provisional v1 COMPLETE
Bare KA11 machine-layer research COMPLETE
Core-only execution/RAM-layout contract v1 COMPLETE (provisional)
Core-only filesystem/kernel data-structure contract v1 COMPLETE (provisional)
Repository-aware first implementation slice NEXT (inspection/planning only)
All named future workstreams NOT STARTED
```

Completion commits verified in Git:

- Stage 0 import: `5e9221ed27fc16acee98914472e7c48452933004`
- Stage 0 static closure: `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
- Stage 1 characterization: `9077f6a6a124682f22a0de79a5cbfd48416de0d3`
- PDP-7 account policy: `c62888eee0b3a1a1abb8613bbe58c09bbcdf8742`
- Stage 2 oracle: `51fcfb34c39fdbf68c9a87f08c9932263cf80668`
- Stage 3A nucleus: `5908c81a1a88193b7510144a3bc44994e8a84ad8`
- Stage 3B / Stage 3 closure: `134b2a7e9a28c061c427620f623be01fb0e19af4`
- Stage 4A I/O substrate: `1caacfe7a87411f4c47317dd06834b1c374a962f`
- Stage 4A machine checkpoint: `1143e4de12138bd9a18c9afcf627038478b7991e`
- PDP-7 terminal/case clarification: `cb81e3393cce3470c2af1981965f1716f40fb978`
- Stage 4B symbol engine and machine checkpoint:
  `313ba822d1e962b4bba2360805717820db61a0c5`
- Stage 4C encoder/open checkpoint:
  `b3414a051761ba1ddadc4a54081a207aa3fa2371`
- Stage 4C capacity characterization:
  `9ad806b0c66a546ef48b43d559d619bdb3251eb7`
- Stage 4C completion/machine checkpoint:
  `b0379f3548c309d464d23dbcc5fb1178b19ccbe6`

## What has been demonstrated

- **Stage 0:** `machines/pdp7` is the persistent project host; `../PDP-7`
  remains the reference machine. Machine provenance and deterministic
  late-summer PDP-11 setup are captured.
- **Stage 1:** the reconstructed PDP-7 B compiler/runtime was inventoried and
  representative constants, storage, arithmetic, branching, loops, calls,
  arguments, vectors/indirection, and `.write` compiled and executed. Ten
  final valid captures used `dmr` because authentic hard-linked runtime files
  created ownership/link constraints; the semantic evidence remains valid.
  Future development normally uses `shankao`.
- **Stage 2:** `tools/pdp11_oracle.py` verifies all eight KA11 addressing
  modes, required instructions/extensions/branches, octal and little-endian
  representation, DEC gold vectors, and the project bootstrap. It rejects
  `MUL/DIV/ASH/ASHC/SOB/XOR`. KE11 remains absent and software arithmetic is
  required.
- **Stage 3:** the bare 24 KB PDP-11/20 executed the R3 threaded PC, R4
  frame/display pointer, and R5 expression-stack architecture. Stage 3A
  demonstrated `c`, `x`, `va`, `b12`, and `b1`; A/B/C/D tests covered
  constants/add, external rvalue, assignment, and automatic lvalue. Stage 3B
  added `f`, `tra`, `b4`, `mark`, `call`, `set`, automatic rvalue `a`, `n11`,
  and `retv`. E/F conditionals, G loop (`123`), H synthetic return, I/J
  one/two arguments, K value return, L nested call, and M real void return all
  passed. Two simultaneously active frames unwound correctly. See
  [`PDP11-B-RUNTIME.md`](PDP11-B-RUNTIME.md) and `evidence/stage3a/` and
  `evidence/stage3b/`.
- **Stage 4A:** a separately maintained B-callable `rewind` helper used the
  authentic PDP-7 `seek` syscall, cleared pending `iflg`, and forced a fresh
  refill with `cibufp = eibufp`. On authoritative `machines/pdp7` as
  `shankao`, a 378-character native B test passed odd mid-buffer and
  cross-refill rewinds, observed EOF as `004`, restarted after EOF, and wrote
  all five required six-digit octal values exactly. See
  [`PDP7-AS11.md`](PDP7-AS11.md) and `evidence/stage4a/`.
- **Stage 4B:** class-B `src/pdp7/as11/as11.b` performs an internal pass 1,
  Stage-4A rewind, and pass 2 on the authoritative PDP-7. It scans the frozen
  assembly-like language, maintains a PDP-11 byte-address location counter,
  resolves forward/backward globals and repeated `0:`–`9:` locals, evaluates
  restricted expressions, and emits deterministic semantic traces without
  PDP-11 instruction encoding. Three positive native fixtures and thirteen
  negative fixtures passed. The largest is 604 host bytes with 48 globals and
  10 local definitions; capacity is 64/64. Stage 3 demand is 17 globals and 5
  local definitions. See [`PDP7-AS11.md`](PDP7-AS11.md) and
  `evidence/stage4b/`.
- **Stage 4C:** PDP-7 B encodes all Stage-3-required KA11
  mnemonics, all eight addressing modes, PC-special forms, extension words,
  branches, JMP/JSR/RTS, and deterministic `i`/`x`/`w` traces. The fixed
  encoding fixture and 18 rejection fixtures passed against the Stage 2
  oracle, as did the normal Stage 4B positive regression. The 48-global,
  10-local Stage 4B substantial fixture fails with an empty result because
  the 3,696-word executable and maximum-capacity symbol arena leave only
  five PDP-7 words between the upward-growing B stack and live symbol data.
  This remains a documented capacity finding for the final `as11` integration
  gate, not a loss of Stage 4B language semantics. See `evidence/stage4c/`.
  This inventory is a validated encoder nucleus and B-bootstrap test corpus,
  not the final historically derived `as11` or UNIX-migration requirement.

The completed Stage 4C authoritative PDP-7 image is 4,096,000 bytes with
SHA-256 `d9a40b9ca80b1f9fa6623947faba1e0097ff8042d12d8e75236eb9b9081de245`.
Capacity runs changed only retained native fixtures/results; closure added
only the reviewed native `shankao/readme`. The installed `as11` source and
executable were reused.
Read-only `fsck7` exited 0 with the already-understood inode-38/block-2987
self-revisit diagnostic. The completion checkpoint and corresponding Stage 4C
experiential era do not change encoder logic or capacity limits.

Focused native characterization now establishes a safe tested point of 38
globals/10 numeric locals; 39 globals passes only with zero locals and fails
with one or more. A realistic Stage-3-shaped 17-global/5-local input passes all
required encodings with 160 words between the B stack label and global arena,
105 more than the 38/10 case. The 48/10 failure is a capacity regression, not
loss of Stage 4B semantics. Stage 4C therefore passes its encoder and current
bootstrap-feasibility contract. No capacity reduction has been accepted;
final capacity and clean exhaustion behavior belong to the Unix-driven
`as11` completion gate.

The provisional v1 migration corpus is now frozen in
[`UNIX-MIGRATION.md`](UNIX-MIGRATION.md). It selects responsibilities rather
than whole-file transliteration from A1-derived `s1.s`–`s8.s`, defers `s9.s`,
and selects `cat` (A1-derived) plus `ls`, `rm`, `sh`, and `stat` (A2-derived)
in their restored B forms, with local C interpretation recorded where needed.
This is the immediate workload for machine-contract and later assembler
requirements, not a claim that the exact December-1970 source set survives.

The core-only contract is deliberately PDP-7-shaped: `fork`, `exit`, minimum
`smes` synchronization, manual child-image loading, six selected file
operations plus `status`, a single-directory RAM-backed filesystem, console
special file, and a possible two-process shell/child execution model. Modern
`exec`, `wait`, full pathnames, persistent RF11 storage, and broader scheduling
remain deferred pending their own evidence gates.

The bare KA11 machine-layer research gate is complete in
[`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md). The PDP-11/20 has no
hardware user/kernel protection modes: system and user code share one physical
address space by software convention, and TRAP changes control flow without a
privilege transition or automatic kernel-stack switch. Installed 24 KB RAM is
`000000`–`057777`; the I/O page is `160000`–`177777`; intervening addresses are
nonexistent on this configuration. The contract records R0–R5/SP/PC/PS process
state, TRAP `104400`–`104777` at vector 034/036 with current-stack PC/PS save,
RTI, and KL11 registers `177560`–`177566`, vectors 060/064, and BR4.

Initial reconstruction scope uses vectors 004/034/060/064, targets
interrupt-driven KL11 for UNIX while allowing polling diagnostics, and does
not require a clock scheduler. Low system placement, one active user image,
software state save, and replaceable RAM process/filesystem backing are
conservative choices. Exact system/user/storage boundaries, RAM geometry, and
the active user-window size were deliberately left unfrozen by that hardware
gate; the later V1 16 KB / 8 KB split is descendant evidence only. The
following execution contract now selects provisional reconstruction values.

The provisional core-only execution/memory contract v1 is complete in
[`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md). It selects, as
conservative reconstruction, a 12 KB system envelope (`000000`–`027777`), a
4 KB fixed user window (`030000`–`037777`, initial SP `040000`), and an 8 KB
shared RAM arena (`040000`–`057777`). A soft `036000` static-image limit leaves
about 1 KB for stack, arguments, and a shell loader; translated sizes remain
empirical gates.

Commands are provisionally raw absolute images loaded and entered at `030000`
by the child shell, not later `a.out` files handled by kernel `exec`. The
symbolic TRAP ABI preserves PDP-7 inline arguments, R0 result/input roles, and
R0=`-1` errors while leaving syscall numbers unfrozen. PDP-7 source establishes
child-first `fork`; one resident user, minimal `smes`, compact live-image/stack
backing, and no clock scheduler form the conservative first process model.
The RAM arena provisionally comprises sixteen 512-byte blocks, and direct-only
files are capped at 4096 bytes. Exact structures and filesystem/process
allocation were left to the follow-on contract summarized next.

The provisional core-only filesystem/data-structure contract v1 is complete
in [`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md). It preserves
the PDP-7 model of ten lowest-free three-word descriptors copied with each
process, a single current inode rather than an inode cache, and negative link
counts. Its reconstructed PDP-11 inode is twelve words / 24 bytes with eight
direct blocks and byte size; the directory entry is a qualified 10-byte
16-bit-inode/eight-byte-name adaptation; and `status` remains the compact
thirteen-word inode-plus-number result. No global open-file table is present.

RAM block 0 holds sixteen inode slots, block 1 the fixed one-block root, and
blocks 2–15 form a common filesystem/process-backing arena managed with one
16-bit block map; a second map covers inodes. V1 also budgets two 64-word
process records and one 512-byte filesystem buffer. Obvious mutable resident
data is estimated below 1 KB, but kernel fit is unproven. The initial image,
shell backing, and writable headroom must fit all sixteen blocks. First
Edition's richer inode/stat/persistent metadata remains descendant evidence,
and RF11 may evolve metadata while preserving high-level algorithms and block
I/O.

The Stage 4A authoritative machine checkpoint is included at HEAD. Read-only
`fsck7` completed with no consistency warning. `image-shankao.fs` is 4,096,000
bytes with SHA-256
`ab6494ab9c3f786544533ff2cd9a054e639f64d8e5095eb4473bd4c965e6cab0`.
The native `shankao` directory retains the working runtime copies, `io.b`,
`rewind.s`, 378-character input, generated `io.s`, linked `a.out`, and result.

The Stage 4B checkpoint supersedes that machine state. The 4,096,000-byte
`image-shankao.fs` has SHA-256
`3543d5a5e055072c9c99af0204a01479caa62b62442dc84b8c08d2631dad4c5a`.
It retains `as11.b`, generated `as11.s`, linked `a.out`, `rewind.s`, runtime
working copies, final fixtures/results, and the combined `probe.s`/`probe.o`.
`fsck7` exits 0. Its sole diagnostic is a checker self-revisit: large-directory
indirect block 2987 is marked in the inode scan and again when inode 38
(`dd/shankao`) is traversed; debug output shows no distinct second owner and no
other consistency warning.

Directly explorable PDP-7 states for Stage 0, Stage 1, Stage 4A, Stage 4B, and
Stage 4C
are materialized under `eras/`. Each PDP-7-only directory now carries its own
recovered bootstrap and SIMH configuration as well as the filesystem image.
Stage 1/4A/4B remain exact checkpoint images; the Stage 0 image has intentional
post-materialization user changes, recorded separately from its source hash in
its README. This experiential layer is distinct from the normal per-gate
authoritative image checkpoints. A representation for PDP-11 RAM, tape, disk,
or paired-machine eras remains deliberately undecided. Beginning
the Stage 4C checkpoint, the native `shankao` directory contains a short
`readme` describing the machine's current capabilities; none was inserted
retroactively into the older exact images.

The active reconstructed frame convention is word 0 previous R4, word 1
saved caller R3 (or returned value after `retv`), and word 2 onward arguments,
automatics, and expression space. Only base KA11 instructions were used. No
disk, UNIX, paper tape, KE11, EIS, or later hardware participated. SIMH
deposits and capture harnesses are class M and are not the final workflow.

## Authoritative machines

- `machines/pdp7`: persistent PDP-7 project host. Preserve its `shankao`
  account, exploratory files, hard-linked authentic files, and filesystem
  image. It is an evolving host used directly for normal development; each
  passing PDP-7 development substage normally commits its image checkpoint.
- `machines/pdp11`: checked-in target configuration, PDP-11/20, 24 KB, no
  disk and no KE11. Stage 3 executions affected volatile RAM only and exited.
- `../PDP-7`: read-only pre-transition/reference machine; never use it for
  project sessions or modify it.
- `../PDP-11`: external reference location; do not modify it.

Fresh-state details, emulator revisions, device settings, image hashes, and
the nonpersistent bootstrap evidence are in [`STATE.md`](STATE.md).

## Provenance confidence and unresolved history

Directly attested facts include PDP-7 cross-development, a B-written PDP-11
assembler on that host, paper tape physically moved to the PDP-11, B running
before UNIX, early `dc`, a core-only/RAM-filesystem system before disk, and
disk arrival around December 1970.

Thompson’s January 1972 B manual is authentic, strong implementation evidence
for R3/R4/R5, threading, frames, address scaling, and several fragments, but
postdates the target. Early/V1 `obrt1` archaeology corroborates parts of the
runtime but is not diskless-1970 source. Stage 3 call entry, control, and value
return are class B reconstruction; `n11` is B/C archaeological evidence.

Not currently known to survive:

- original 1970 B-written `as11` source;
- exact PDP-7-hosted PDP-11 B cross-compiler source;
- exact diskless-1970 PDP-11 B runtime source;
- PDP-7/early B source of the first `dc`;
- exact Bell Labs tape encoding/loading convention;
- exact core-only PDP-11 UNIX kernel source.

The current RF11 plus one RS11 disk identification is a strong hypothesis,
not proof of the exact Bell Labs physical unit. DEC Absolute Binary/Absolute
Loader is only a possible class-C fallback if the Bell convention remains
unknown; it is not established Bell Labs practice.

## Remaining roadmap and risk boundary

The migration corpus and provisional machine, execution/RAM, and
filesystem/data-structure contracts are complete. The next gate inspects the
actual repository and produces a bounded plan for the first implementation
slice; it does not authorize coding automatically. After that, two dependency
tracks can advance: bootstrap work (`as11`, threaded B, `b11`, paper tape,
calculator, and `dc0`) and
migration of selected PDP-7 kernel and command responsibilities through a
bare-machine substrate into core-only
PDP-11 UNIX. They converge on the PDP-11 and then on the December 1970 disk
transition. See [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md).

`as11` and `b11` are medium technical risk with material historical
uncertainty. Tape transport is technically bounded but its exact Bell encoding
is unknown. `dc0` has high historical uncertainty. Core-only UNIX is very high
technical and historical risk and may fail without invalidating the completed
or “Across the Floor” milestones. See PLAN’s risk table.

## Do not do yet

- Do not implement `b11`, tape records/loaders, `dc0`, or any UNIX stage.
- Do not port `s1`–`s8` responsibilities or commands during the
  repository-aware planning gate.
- Do not treat the provisional memory boundaries or RAM-block geometry as
  recovered history, or mistake the common dynamic arena for a historically
  attested fixed filesystem/process partition.
- Do not add assembler instructions/directives merely to broaden Stage 4C;
  derive final `as11` requirements from selected migration workloads.
- Do not start the Stage-3 gold round trip before the integrated assembler gate.
- Do not merge assembler, compiler, and paper-tape responsibilities.
- Do not enable KE11/EIS, attach disk/tape, or substitute a later UNIX system.
- Do not modify either reference tree; use authoritative `machines/pdp7` as
  `shankao` for authorized Stage 4 development and preserve shared originals.
- Do not repeat broad historical research already recorded here and in
  SOURCES; investigate only a newly identified unresolved question.

## Resume here

Perform the **repository-aware first implementation-slice** inspection and
produce a plan before coding. Establish the exact current Stage-4C syntax and
features, Stage-3 PDP-11 loading/execution harness, artifacts and oracle
integration, then order vectors, trap entry, KL11 polling/interrupts,
RAM/block abstraction, filesystem nucleus, process control, and commands.
Identify bounded non-speculative tests and when a persistent PDP-11 era first
becomes meaningful. Use [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md),
[`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md),
[`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md), and
[`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md) as fixed
inputs. Do not automatically begin implementation, add assembler features,
assign syscall numbers, fix capacity, or start `b11`, tape, `dc`, or UNIX.
