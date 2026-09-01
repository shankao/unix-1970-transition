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
Stage 4  NEXT — NOT STARTED
Stages 5–12  NOT STARTED
```

Completion commits verified in Git:

- Stage 0 import: `5e9221ed27fc16acee98914472e7c48452933004`
- Stage 0 static closure: `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
- Stage 1 characterization: `9077f6a6a124682f22a0de79a5cbfd48416de0d3`
- PDP-7 account policy: `c62888eee0b3a1a1abb8613bbe58c09bbcdf8742`
- Stage 2 oracle: `51fcfb34c39fdbf68c9a87f08c9932263cf80668`
- Stage 3A nucleus: `5908c81a1a88193b7510144a3bc44994e8a84ad8`
- Stage 3B / Stage 3 closure: `134b2a7e9a28c061c427620f623be01fb0e19af4`

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

The active reconstructed frame convention is word 0 previous R4, word 1
saved caller R3 (or returned value after `retv`), and word 2 onward arguments,
automatics, and expression space. Only base KA11 instructions were used. No
disk, UNIX, paper tape, KE11, EIS, or later hardware participated. SIMH
deposits and capture harnesses are class M and are not the final workflow.

## Authoritative machines

- `machines/pdp7`: persistent PDP-7 project host. Preserve its `shankao`
  account, exploratory files, hard-linked authentic files, and filesystem
  image; commit image versions only at meaningful milestones.
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
- Do not merge assembler, compiler, and paper-tape responsibilities.
- Do not enable KE11/EIS, attach disk/tape, or substitute a later UNIX system.
- Do not modify either reference tree or historical machine merely for fresh
  evidence; use `machines/pdp7` as `shankao` only when Stage 4 authorizes it.
- Do not repeat broad historical research already recorded here and in
  SOURCES; investigate only a newly identified unresolved question.

## Resume here

Investigate and design **Stage 4 `as11`** as a separately scoped change. Read
the Stage 4 gate in PLAN, inventory the locally recorded assembler evidence,
define the smallest input/object boundary needed to reproduce Stage 3 words,
and plan PDP-7 execution under `shankao`. Do not implement `b11`, paper-tape
transport, `dc`, or UNIX, and do not begin Stage 4 implementation as part of
this documentation milestone.
