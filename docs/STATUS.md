# Project Status

This is the authoritative checkpoint for resuming work. Detailed policy,
roadmap, machine evidence, sources, and decisions remain in
[`METHOD.md`](METHOD.md), [`PLAN.md`](PLAN.md), [`STATE.md`](STATE.md),
[`SOURCES.md`](SOURCES.md), and [`DECISIONS.md`](DECISIONS.md).

## Goal and historical point

Reconstruct, with explicit provenance, the 1970 workflow that used PDP-7 UNIX
and B-hosted tools to prepare threaded B programs for a newly delivered,
diskless PDP-11/20. The frozen target is the late-summer/pre-disk transition,
not First Edition UNIX.

## Current stage and gate

**Stage 1 — complete; gate passed.** The repository now contains an observed
interface specification showing representative B source passing through the
reconstructed compiler, emitted threaded assembly, surviving runtime, and
native execution. **Stage 2 is next and has not started.** Stages 3–10 also
have not started.

## Completed work

- **Stage 0 — complete.** `5e9221ed27fc16acee98914472e7c48452933004`
  imported the persistent PDP-7 host; `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
  closed the static reproducibility capture. See `STATE.md` and
  `evidence/pdp7-import-manifest.tsv`.
- **Stage 1 — complete at this checkpoint.** The static audit, designed probe
  corpus, captured emissions, native results, and interface mapping are in
  `B-BASELINE.md` and `evidence/pdp7-b-stage1-results.tsv`.

## Authoritative machines

- `machines/pdp7`: authoritative persistent PDP-7 project host. Preserve its
  `shankao` account, exploratory files, and filesystem image.
- `machines/pdp11`: checked-in PDP-11 configurations; the target remains an
  unbooted 11/20 with 24 KB, no disk, and no KE11.
- `../PDP-7`: read-only pre-transition/reference machine; never use it for
  project sessions or modify it.
- `../PDP-11`: external reference location; do not modify it.

The PDP-7 uses Open SIMH V4.0-0 (`aad53510`), 8K words, EAE, RB09 image
`image-shankao.fs`, and enabled/unattached PTR/PTP at fresh startup. The PDP-11
uses a locally replaced Open SIMH V4.0-0 (`8a4b3752`); `pdp11.conf` preserves
the earlier static configuration, while `late-summer-1970.simh`
deterministically encodes the intended configuration and observed 14-word
bootstrap without running it. The former live PDP-11 session was exited and
its deposited RAM is considered gone.

## Provenance and established history

Use A/B/C/D/M exactly as defined in `METHOD.md`. The imported restoration mixes
scan-derived surviving material with later restoration code and local machine
state; it is not uniformly original Bell Labs source. The current PDP-7 B
compiler is understood provisionally as reconstruction (B) until Stage 1
records it file by file. Emulator/configuration/test automation is modern (M).

Primary accounts establish that the PDP-11 arrived before its disk; Bell Labs
used B threaded-code operator fragments, a B-written PDP-11 assembler running
on the PDP-7, physical paper-tape transfer, and an early `dc`. Exact lost
implementations are not thereby recovered. See `SOURCES.md`.

Accepted reconstruction/substitution policy: conservative lost-component
reconstruction is B; later archaeological material is comparison evidence, not
proof; a contemporary DEC tape format may eventually be C, but none has been
selected. The exact Bell Labs tape encoding, diskless PDP-11 runtime,
cross-assembler source, backend conventions, and earliest `dc` remain
unresolved (D where evidence is insufficient).

## Stage 1 result and remaining unknowns

Stage 1A is complete. The surviving `bi.s`/`bl.s` scan transcriptions are A;
their runnable restoration copies contain small changes and are B. The working
compiler is Robert Swierczek's 2016 reconstructed `b.b`, installed as
`/system/b`; it is B and its executable matches `build/bin/b` word-for-word.
The installed invocation is `b source.b output.s`, then
`as op.s bl.s output.s bi.s`, then `a.out`. A stale host-side readme instead
says `bc`/`ops.s`; no installed `bc` exists. No `shankao` B source was found;
its `hello.s` is direct assembly. See `B-BASELINE.md` and the inventory TSV.

Stage 1B's class-M probes cover constants, storage, arithmetic,
comparisons/branches, loops, zero- and two-argument calls, vectors,
indirection, and `.write`. Ten synchronized probes passed native end to end:
`s2`, `b4`, `l5`, `c6`, `g7`, `e9`, `c1`, `a3`, `v8`, and `i8`. Captured
emissions map these constructs to `consop`, `binop`, `setop`, branch, call,
vector/indirection, and library machinery. Four earlier queued console
transfers were corrupt and are retained separately; they are not compiler
failures. No compiler/runtime repair was attempted.

Remaining technical limits are explicit: shift behavior is not in the
demonstrated subset; only `.write` was dynamically exercised among the
library entries; and the reconstructed host compiler needs GNU89 mode with the
current GCC. These do not block the representative Stage 1 gate. Exact hashes,
emissions, outputs, and the resulting interface contract are in
`B-BASELINE.md` and the Stage 1 evidence directories. The PDP-7 was shut down
cleanly. The PDP-11 was neither booted nor modified.

Do **not** begin a PDP-11 backend, cross-assembler, loader/tape format,
PDP-11 runtime, Stage 2 oracle, or `dc`; do not modify or boot the PDP-11; do
not modify the existing PDP-7 compiler/runtime merely to pass probes.

## Resume here

Begin Stage 2 only in a new, separately scoped change: build the modern
verification oracle described in `PLAN.md`, using the Stage 1 interface in
`B-BASELINE.md` as its input contract. First update this checkpoint to mark
Stage 2 current. Do not infer a PDP-11 backend or historical tape format from
the probe results, and do not boot or modify the PDP-11 merely to start Stage
2.
