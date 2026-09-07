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
working reconstructed standalone threaded-B execution model. The repository’s
eventual boundary is the first disk-backed PDP-11 UNIX environment consistent
with the December 1970 disk arrival—not the rest of 1971 or First Edition.

## Current stage

```text
Stage 0  COMPLETE
Stage 1  COMPLETE
Stage 2  COMPLETE
Stage 3  COMPLETE (3A and 3B)
Stage 4  IN PROGRESS
Stage 4A COMPLETE
Stage 4B COMPLETE
Stage 4C COMPLETE
Stages 4D–4E NOT STARTED
Stages 5–12 NOT STARTED
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
  This remains a documented capacity finding for Stage 4D, not a loss of
  Stage 4B language semantics. See `evidence/stage4c/`.

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
final capacity and clean exhaustion behavior belong to Stage 4D.

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

Phase II reconstructs `as11` (Stage 4), `b11` (5), integrates them with
modern loading (6), establishes real tape transport (7), and completes the
“Across the Floor” loop (8). Phase III builds a small RPN calculator (9) and
historically constrained `dc0` (10). Phase IV tackles core-only/RAM-filesystem
UNIX (11). Phase V models disk arrival and the first disk-backed system (12).

`as11` and `b11` are medium technical risk with material historical
uncertainty. Tape transport is technically bounded but its exact Bell encoding
is unknown. `dc0` has high historical uncertainty. Core-only UNIX is very high
technical and historical risk and may fail without invalidating the completed
or “Across the Floor” milestones. See PLAN’s risk table.

## Do not do yet

- Do not implement `b11`, tape records/loaders, `dc0`, or any UNIX stage.
- Do not start Stage 4E execution before Stage 4D's integrated assembler gate.
- Do not merge assembler, compiler, and paper-tape responsibilities.
- Do not enable KE11/EIS, attach disk/tape, or substitute a later UNIX system.
- Do not modify either reference tree; use authoritative `machines/pdp7` as
  `shankao` for authorized Stage 4 development and preserve shared originals.
- Do not repeat broad historical research already recorded here and in
  SOURCES; investigate only a newly identified unresolved question.

## Resume here

Investigate and finalize **Stage 4D's bootstrap-sufficient output/resource
design before implementation**. Replace the diagnostic trace with the final
textual address/word map, measure the resulting executable against realistic
bootstrap inputs, and design clean native memory-exhaustion behavior with an
adequate safety margin. Do not assume 38 globals is universally safe, and do
not start Stage 4E, `b11`, tape, `dc`, or UNIX.
