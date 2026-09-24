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

The demonstrated point is the diskless late-1970 PDP-11/20. In addition to the
standalone threaded-B and U1 machine programs, a first core-only Unix increment
now runs a translated `cat`: it opens `readme` in a RAM filesystem, reads the
file through Unix calls, writes it through the tty special file, closes it, and
exits. The surviving/restored PDP-7 UNIX system is the principal source base
for this migration. The repository's eventual boundary is the first
disk-backed PDP-11 UNIX environment consistent with the December 1970 disk
arrival—not the rest of 1971 or First Edition.

## Current stage

The checklist below tracks reconstruction work, not public historical-state
boundaries. The [running guide](RUNNING.md) now leads through working PDP-7
Unix, hands-on PDP-11 assembly on PDP-7, and tape-loaded console interaction
on the diskless PDP-11. Existing directory names and machine states are kept.
Native assembly and visitor export are now one continuous path: `as11` creates
the trace on the era disk, `punch_era.py` invokes its native `abspun` through
PTP, and the generated replay feeds the exact tape through PDP-11 PTR and the
class-C DEC loader. B4/U1 remain complete. The first interleaved U2/U3/U4
increment is complete, while all three parent groups remain incomplete.

Manual checks passed: both PDP-7 logins and `ls`, the documented small
native assembly and exact 131-word console reassembly (on disposable era
copies), direct PTR replay with `AB` and `ki`, and the optional RAM replay.
The `punch_era.py` test exercised the documented
`101` -> `102` native edit, produced three exact words, punched 74 bytes in
four valid DEC records, loaded them through PTR/bootstrap/Absolute Loader, and
observed R0 `000102`. The Unix build uses a disposable copy of the
cross-development image. A separate, explicit installation updated the living
era's `as11` after its new instructions and smaller runtime buffers passed the
native tests. Current test totals are recorded with this increment below.

- [x] **Historical/bootstrap foundation**
  - [x] Stage 0 — machine reproducibility
  - [x] Stage 1 — PDP-7 B characterization
  - [x] Stage 2 — independent KA11 oracle
  - [x] Stage 3 — standalone threaded-B PDP-11 execution (3A/3B)
  - [x] Stage 4A — B I/O/two-pass support
  - [x] Stage 4B — scanner/parser/symbol/expression engine
  - [x] Stage 4C — KA11 encoder nucleus
- [x] **R1–R5 migration research/contracts**
  - [x] Provisional migration corpus v1
  - [x] Bare KA11 machine-layer contract
  - [x] Provisional core-only execution/RAM-layout contract v1
  - [x] Provisional filesystem/kernel data-structure contract v1
  - [x] Repository inspection before implementation
- [ ] **B1 — Workload-driven as11 closure** — IN PROGRESS.
  - [x] B1.1 — Native as11 -> exact KA11 execution
  - [x] B1.2 — First workload-driven extensions: `rti`, `trap`, `bit`, `bic`,
    `bis`
  - [ ] B1.3–B1.6 — workload additions, final contract, realistic capacity,
    and clean exhaustion/safety envelope
- [ ] **B2–B3 and B5–B7 bootstrap work** — future, independently
  dependency-gated.
- [x] **B4 — Paper-tape transport** — complete.
  - [x] B4.0 — Conservative DEC bootstrap/Absolute Loader contract frozen
  - [x] B4.1–B4.4 — PDP-7 tape production, PDP-11 reader/loader, memory
    identity, and historical acceptance execution
- [x] **U1 — Bare PDP-11 machine substrate** — complete.
  - [x] U1.1 — Stage-3 gold round trip
  - [x] U1.2 — KL11 polling input/output
  - [x] U1.3 — Low-core vectors + RTI
  - [x] U1.4 — Interrupt-driven KL11 console
  - [x] U1.5 — TRAP/syscall entry and return
  - [x] U1.6 — RAM storage primitive
  - [x] U1.7 — Historical/mechanical-load acceptance
- [ ] **U2 — Filesystem nucleus** — IN PROGRESS. RAM initialization, fixed-root
  lookup, one current inode, direct-block reads, descriptors, read-only
  `open`, `read`, `close`, and ttyout `write` now support the first `cat` run.
  Creation, ordinary-file writes, mutation, tty input, and full U2 acceptance
  remain.
- [ ] **U3 — Process/execution nucleus** — IN PROGRESS only to the extent that
  the directly started command can call a minimal `exit`. Fork, parent backing,
  command loading, synchronization, and U3 acceptance remain.
- [ ] **U4 — Minimal userland** — IN PROGRESS. U4.1 `cat` is complete in its
  first fixed-name form; the other commands and full U4 acceptance remain.
- [ ] **U5–U7 Unix integration and disk transition** — future work remains
  open.
- [x] Canonical active machine configs
- [x] Historical-era and reconstruction-snapshot semantics separated
- [x] Three current historical-system eras made directly runnable
- [x] Stable R1–R5 / B1–B7 / U1–U7 hierarchy recorded
- [x] Licensing/provenance policy frozen before U2 implementation

Completion commits verified in Git:

- Stage 0 import: `5e9221ed27fc16acee98914472e7c48452933004`
- Stage 0 static closure: `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
- Stage 1 characterization: `9077f6a6a124682f22a0de79a5cbfd48416de0d3`
- PDP-7 account policy: `c62888eee0b3a1a1abb8613bbe58c09bbcdf8742`
- Stage 2 oracle: `51fcfb34c39fdbf68c9a87f08c9932263cf80668`
- Stage 3A nucleus: `5908c81a1a88193b7510144a3bc44994e8a84ad8`
- Stage 3B / Stage 3 closure: `134b2a7e9a28c061c427620f623be01fb0e19af4`
- Stage 4A I/O support: `1caacfe7a87411f4c47317dd06834b1c374a962f`
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
  PDP-11 instruction encoding. Three positive native tests and thirteen
  negative tests passed. The largest input is 604 host bytes with 48 globals
  and 10 local definitions; capacity is 64/64. Stage 3 demand is 17 globals and
  5 local definitions. See [`PDP7-AS11.md`](PDP7-AS11.md) and
  `evidence/stage4b/`.
- **Stage 4C:** PDP-7 B encodes all Stage-3-required KA11
  mnemonics, all eight addressing modes, PC-special forms, extension words,
  branches, JMP/JSR/RTS, and deterministic `i`/`x`/`w` traces. The fixed
  encoding test and 18 rejection tests passed against the Stage 2
  oracle, as did the normal Stage 4B positive regression. The 48-global,
  10-local Stage 4B large test fails with an empty result because
  the 3,696-word executable and maximum-capacity symbol arena leave only
  five PDP-7 words between the upward-growing B stack and live symbol data.
  This remains a documented capacity finding for the final `as11` integration
  gate, not a loss of Stage 4B language semantics. See `evidence/stage4c/`.
  This inventory is a validated encoder nucleus and B-bootstrap test corpus,
  not the final historically derived `as11` or UNIX-migration requirement.

The completed Stage 4C authoritative PDP-7 image is 4,096,000 bytes with
SHA-256 `d9a40b9ca80b1f9fa6623947faba1e0097ff8042d12d8e75236eb9b9081de245`.
Capacity runs changed only retained native test inputs and results; closure
added only the reviewed native `shankao/readme`. The installed `as11` source and
executable were reused.
Read-only `fsck7` exited 0 with the already-understood inode-38/block-2987
self-revisit diagnostic. The completion checkpoint and corresponding Stage 4C
reconstruction snapshot do not change encoder logic or capacity limits.

Focused native characterization now establishes a safe tested point of 38
globals/10 numeric locals; 39 globals passes only with zero locals and fails
with one or more. A realistic Stage-3-shaped 17-global/5-local input passes all
required encodings with 160 words between the B stack label and global arena,
105 more than the 38/10 case. The 48/10 failure is a capacity regression, not
loss of Stage 4B semantics. Stage 4C therefore passes its encoder and current
bootstrap-feasibility contract. No capacity reduction has been accepted;
final capacity and clean exhaustion behavior belong to the workload-driven
B1 `as11` closure gate.

The subsequent Stage-3 gold integration checkpoint evolves the authoritative
image to SHA-256
`5ce0c014a19f25242893dcc3f0ab7a654a819d263732b50253332dbaf4e7c3f2`.
It retains native `gold.s` and `gold.o`; no preserved era image changed.
Read-only `fsck7` still exits 0 with only the known inode-38/block-2987
self-revisit.

The KL11 polling diagnostic is assembled by that same native PDP-7 `as11`
path. Its 33-word trace contains 19 oracle-verified instructions using
absolute I/O-page addresses. Controlled, non-PTY-echoed input `A` then `B`
produced device output `AB`; saved RAM words independently retained octal
`000101` and `000102`, and the program halted at `001076`. The reproducible
manual deposit file is `artifacts/kl11-poll.simh`. This proves polling
only: interrupt enables and vectors 060/064 remain unused.

The retained native `klpoll.s`/`klpoll.o` checkpoint evolves the authoritative
PDP-7 image to SHA-256
`fa9294110e6e66eb5450aa600a5d52b0aba1e9d3d4f25223da67be582181b926`.
Read-only `fsck7` exits 0 with only the established inode-38/block-2987
self-revisit. Exact Stage checkpoint images are preserved under `snapshots/`;
current historical hypotheses are maintained separately.

Active tools now use `machines/pdp7/pdp7.simh` for the unthrottled evolving
PDP-7 host and `machines/pdp11/pdp11.simh` for a clean 24 KB KA11 baseline.
The latter deposits or runs no software, attaches no storage or paper tape,
and does not explicitly enable the clock; this SIMH build exposes CLK as an
inherent non-disableable device. The obsolete volatile-bootstrap setup is no
longer an active configuration.

The five Stage-labelled PDP-7 directories are reconstruction-project
checkpoints under `snapshots/`, not historical era boundaries. The former
polling-only `pdp11-crossdev` files are preserved there as well. The current
historical-system models are `eras/pdp7-unix/`, `eras/pdp7-crossdev/`, and
`eras/pdp11-crossdev/`, each with an `ERA.md` and tested direct replay. The
PDP-11 era consumes committed U1 tapes through PTR, the fourteen-word bootstrap,
and DEC Absolute Loader. It remains cross-developed, not self-hosted or UNIX.

**U1 bare-machine substrate:** two focused class-B/M test programs produced 342
native PDP-7 `as11` words containing 178 Stage-2-decoded instructions. Real
KL11 RX/TX interrupts accepted and echoed `A` then `B`; vectors 060/064 saved
PC/PS on the current stack and three `RTI` sites restored execution. Diagnostic
`TRAP 7` entered vector 034, decoded call 7, consumed inline octal `12345`,
returned octal `12354` in R0, preserved R1/R2, resumed after the inline word,
and restored SP `027000`. This freezes no Unix syscall-number table.

The RAM test program addressed sixteen 512-byte blocks at `040000`–`057777`, kept
blocks 0–1 reserved from allocation, returned distinct blocks 2–15, failed
cleanly on exhaustion, reused freed block 2 for simulated process backing,
and round-tripped all 256 words of a block without changing the next-block
sentinel. It introduces no filesystem or process semantics. Native `as11.b`,
generated `as11.s`, and linked `a.out` are 5,803, 8,454, and 3,779 PDP-7 words;
the 317-word static remainder is not a final capacity claim.

The final authoritative PDP-7 image for U1 is 4,096,000 bytes with SHA-256
`31498835013c176d3015128fdc4d7f3e2586a467918388625615d9d376f93620`.
Read-only `fsck7` exits 0 with only the established inode-38/block-2987
self-revisit. Useful native `u1int.s/.o` and `u1ram.s/.o` remain; the abandoned
oversized `u1diag.s/.o` pair was removed. No preserved era was changed.

### PDP-11 program-production audit

The current living reconstruction follows the native-assembler rule. The
following audit groups describe loading practice, not the A/B/C/D source
provenance classes:

- **Manual-scale deposit:** the PDP-11 paper-tape replays directly enter only
  DEC's fourteen-word bootstrap. This represents plausible front-panel entry.
- **Fast debugging:** the Stage-3 gold, KL11 polling, and U1 direct-load scripts
  deposit exact native PDP-7 `as11` output. Each substantial program has
  readable symbolic source; the host decodes or compares words but does not
  generate the executed image.
- **Incorrect current reconstruction:** none found. The living PDP-11 era
  loads both U1 programs through PTR, the bootstrap, and the Absolute Loader;
  its replay files contain no payload deposits.
- **Reconstruction-history evidence:** the Stage 3A/3B Python fixed-layout
  builders, their SIMH deposit scripts, and the earlier polling snapshot record
  work done before the native assembler path was available. They remain under
  `tools/`, `evidence/`, and `snapshots/` and are not a model for new PDP-11
  programs.

New substantial PDP-11 programs must therefore be written symbolically and
assembled by native PDP-7 `as11`. Direct loading may still repeat that exact
output during debugging. The audit itself changed no machine code or media;
the later `cat` increment follows this rule.

**First core-only Unix command:** nine fixed-address system source files and a
separate `cat` source were assembled by the accepted PDP-7 `as11`. The system
initializes RAM blocks 0–2, finds `readme` in a 30-byte root directory, opens
it on lowest-free descriptor 2, reads its 36 bytes through a 512-byte kernel
buffer in five calls, writes those bytes through ttyout in five calls, closes
the descriptor, and exits cleanly. The console shows
`PDP-11 Unix read this from readme.` followed by CR/LF. The displayed text is
stored in the ordinary RAM file and is not present in `cat`.

The system contains 643 native words and 390 decoded instructions; `cat`
contains 28 words and 16 instructions. Their ten PDP-7-punched tapes total
6,509 bytes. Historical acceptance loaded every tape through PTR, the
front-panel bootstrap, and the DEC Absolute Loader, compared every memory word
with native output, and reproduced the fast run's result. Blocks 3–15 remain
unused; the planned allocation maps are not implemented yet. The calls are
provisional reconstructions: `exit=1`, `open=2`, `read=3`, `write=4`, and
`close=5`.

For scale, 6,509 tape bytes correspond to about 22 seconds at a documented
300-character/second PC11 reader rate, 2 minutes 10 seconds at a
50-character/second PC11 punch rate, or 10 minutes 51 seconds at a
10-character/second Model 33 rate. These are contemporary reference rates,
not evidence for Bell Labs' exact device, and the emulator does not add an
artificial delay.

This work adds `sub`, `beq`, and `dec` to the native assembler. The explicitly
installed era command is 3,788 PDP-7 words and uses 16-word B input/output
buffers. Its global and local tables occupy space released below those smaller
buffers, and the installed command passes the exact Stage-3 gold source.
Normal Unix builds use a disposable copy of the era disk; the final recorded
build left SHA-256
`d2e7cd48703c80096ce64ea04ab55acfb6c219458b17e12261129ff2a212954b`
unchanged. Creation, ordinary-file writes,
tty input, fork, parent restoration, loading commands from the filesystem,
arguments, and a shell remain unimplemented.

All 104 host tests pass. The U1 replay still reports 342 words, 178
instructions, and U1.3–U1.6 PASS. Read-only `fsck7` exits 0 for both changed
PDP-7 images with only the established inode-38/block-2987 self-revisit.

Earlier canonical-config regression runs retained the same useful native
sources and outputs and had advanced the evolving authoritative image to SHA-256
`40905562d9feb63b2a5e95f542098e052c12da7fc9af136098e907c3cb781968`.
Stage 4A, the Stage 4B semantic set below its documented capacity boundary,
Stage 4C encoding/rejection tests, fresh Stage-3 gold `D`, and fresh KL11 `AB`
all passed. Read-only `fsck7` again exited 0 with only the known self-revisit.

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
working copies, final test inputs and results, and the combined
`probe.s`/`probe.o`.
`fsck7` exits 0. Its sole diagnostic is a checker self-revisit: large-directory
indirect block 2987 is marked in the inode scan and again when inode 38
(`dd/shankao`) is traversed; debug output shows no distinct second owner and no
other consistency warning.

Directly explorable project states for Stage 0, Stage 1, Stage 4A, Stage 4B,
and Stage 4C are materialized under `snapshots/`. Their original README,
bootstrap, configuration, and filesystem media remain intact. Stage 1/4A/4B
remain exact checkpoint images; the Stage 0 image has intentional
post-materialization user changes recorded separately from its source hash.
They document reconstruction history and are not asserted as five Bell Labs
historical eras. Current historical hypotheses instead live under `eras/` and
may evolve with recorded evidence. Beginning
the Stage 4C checkpoint, the native `shankao` directory contains a short
`readme` describing the machine's current capabilities; none was inserted
retroactively into the older exact images.

The active reconstructed frame convention is word 0 previous R4, word 1
saved caller R3 (or returned value after `retv`), and word 2 onward arguments,
automatics, and expression space. Only base KA11 instructions were used. No
disk, UNIX, paper tape, KE11, EIS, or later hardware participated. Scripts
that deposit words and capture output are class M and are not the final
workflow.

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
not proof of the exact Bell Labs physical unit. B4 now uses DEC Absolute
Binary/Absolute Loader as the demonstrated class-C substitute; it remains not
established Bell Labs practice.

## Remaining roadmap and risk boundary

The repository now distinguishes two histories. `snapshots/stage-*` preserves
the exact machine states established by modern project milestones; `eras/`
contains three living, capability-based historical hypotheses with concise
manifests and tested human replay. The diskless PDP-11 replay consumes the
unchanged committed U1 tapes through PTR/bootstrap/Absolute Loader. B4 and U1
remain complete. The first Unix increment is an accepted development result,
but is not yet a new public historical state.

The migration corpus and provisional machine, execution/RAM, and
filesystem/data-structure contracts are complete. Repository inspection and
the Stage-3 gold test are complete. Two dependency
tracks can advance: bootstrap work (`as11`, threaded B, `b11`, paper tape,
calculator, and `dc0`) and
migration of selected PDP-7 kernel and command responsibilities through
bare-machine services into core-only
PDP-11 UNIX. They converge on the PDP-11 and then on the December 1970 disk
transition. See [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md).

B4 and U1.7 are complete. Two accepted U1 test programs totaling 342 native
PDP-7-assembled words were punched on the PDP-7, loaded through the PDP-11 PTR,
fourteen-word bootstrap, and 72-word DEC Absolute Loader, compared exactly in
memory, and replayed with their established results. The same method has now
loaded the 643-word Unix system and separate 28-word `cat`, then reproduced
the accepted `readme` output. U2/U3/U4 are completion groups rather than a
required sequence; none of their parents is complete.

`as11` and `b11` are medium technical risk with material historical
uncertainty. Paper-tape loading has limited technical scope, but its exact Bell
encoding is unknown. `dc0` has high historical uncertainty. Core-only UNIX has
very high technical and historical risk and may fail without invalidating the
completed or “Across the Floor” milestones. See PLAN’s risk table.

## Do not do without a clearly scoped task

- Do not extend U2/U3/U4, or begin `b11`, `dc0`, or later Unix work, without an
  explicitly scoped task and its dependency gate.
- Do not finish U2 in isolation merely because it is numbered first. Once the
  first file operations work, use `cat`, then the minimum process and shell
  code, to expose the next real requirement.
- Do not treat the provisional memory boundaries or RAM-block geometry as
  recovered history, or mistake the common dynamic arena for a historically
  attested fixed filesystem/process partition.
- Do not add assembler instructions/directives merely to broaden Stage 4C;
  derive final `as11` requirements from selected migration workloads.
- Do not mistake the completed Stage-3 gold round trip for final `as11`, tape,
  or UNIX integration.
- Do not merge assembler, compiler, and paper-tape responsibilities.
- Do not enable KE11/EIS, attach disk/tape, or substitute a later UNIX system.
- Use authoritative `machines/pdp7` as `shankao` for authorized PDP-7
  development and preserve shared originals.
- Do not repeat broad historical research already recorded here and in
  SOURCES; investigate only a newly identified unresolved question.

## Resume here

Choose the next small Unix behavior from the dependencies exposed by the
accepted `cat readme` run. Do not finish U2 in isolation or broaden the first
implementation merely because adjacent calls are easy. Fast deposits remain
suitable for small debugging. Before another substantial increment determines
what comes next, build it with the PDP-7-side tools, transfer it by paper tape,
and record its code and tape sizes.
