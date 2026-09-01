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

**Stage 3 is in progress: Stage 3A complete and gate passed; Stage 3B is next
and has not started.** The strongly evidenced direct-threaded nucleus executed
successfully on the bare PDP-11/20. Stages 4–10 have not started.

## Completed work

- **Stage 0 — complete.** `5e9221ed27fc16acee98914472e7c48452933004`
  imported the persistent PDP-7 host; `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
  closed the static reproducibility capture. See `STATE.md` and
  `evidence/pdp7-import-manifest.tsv`.
- **Stage 1 — complete at this checkpoint.** The static audit, designed probe
  corpus, captured emissions, native results, and interface mapping are in
  `B-BASELINE.md` and `evidence/pdp7-b-stage1-results.tsv`.
- **Stage 2 — complete at this checkpoint.** `tools/pdp11_oracle.py` and
  `tests/test_pdp11_oracle.py` provide the audited class-M instruction oracle;
  its boundary and use are documented in `PDP11-ORACLE.md`.
- **Stage 3A — complete at this checkpoint.** Class-B `c`, `x`, `va`, `b12`,
  and `b1` fragments plus direct R3 dispatch ran in four class-M deposited
  smoke tests. See `PDP11-B-RUNTIME.md` and `evidence/stage3a/`.

## Authoritative machines

- `machines/pdp7`: authoritative persistent PDP-7 project host. Preserve its
  `shankao` account, exploratory files, and filesystem image.
- `machines/pdp11`: checked-in PDP-11 configurations; the target remains an
  11/20 with 24 KB, no disk, and no KE11. Stage 3A runs changed only volatile
  RAM and each simulator process exited.
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

Account caveat: the ten final valid Stage 1 compiler, assembler/link, and
execution captures were performed under `dmr` after ownership/linking
constraints were encountered while working from `shankao`. They remain valid
Stage 1 behavioral evidence and do not change its conclusions. Future project
development on the persistent PDP-7 should normally use `shankao`, copying
needed working files there without altering authentic shared originals.

Remaining technical limits are explicit: shift behavior is not in the
demonstrated subset; only `.write` was dynamically exercised among the
library entries; and the reconstructed host compiler needs GNU89 mode with the
current GCC. These do not block the representative Stage 1 gate. Exact hashes,
emissions, outputs, and the resulting interface contract are in
`B-BASELINE.md` and the Stage 1 evidence directories. The PDP-7 was shut down
cleanly. The PDP-11 was neither booted nor modified.

## Stage 2 result and Stage 3 boundary

The oracle supports all eight operand modes and PC-special immediate,
absolute, relative, and relative-deferred forms; required extension words;
the project KA11 double/single operand, branch, call/return, condition-code,
and operate subset; signed branch calculation in both directions; and
little-endian serialization. Thirteen unit tests pass, including all supplied
fixed vectors, DEC's exact `CMPB @#177560,#301` gold vector, negative rejection
of later `MUL/DIV/ASH/ASHC/SOB/XOR`, and an address-aware walk of the project
bootstrap that excludes its final data word.

The oracle is class M only and is not part of the eventual historical path.
It is deliberately not an assembler, emulator, symbol system, runtime,
loader, or paper-tape formatter. Stage 3 can use it to verify a class-B
standalone threaded nucleus. Base-target multiplication, division/remainder,
and multi-bit shifts require software routines/loops; neither KE11 nor later
EIS instructions may be assumed. See `PDP11-ORACLE.md`.

## Stage 3A result and Stage 3B boundary

Stage 3A implements the documented R3 threaded PC, R4 frame/display pointer,
R5 expression stack, and `jmp @(r3)+` dispatch. Readable class-B assembly
closely follows Thompson's January 1972 printed `c`, `x`, `va`, `b12`, and
`b1` sequences. That authentic manual postdates the late-1970 target, so this
is conservative reconstruction rather than surviving 1970 source. `aap/b`
`obrt1` is corroborating B/C reference only; no third-party code was imported.

Four fresh bare-PDP-11 executions passed: constant/add printed `A`; external
rvalue printed `B`; word-address assignment printed `C` and left
`003002=000103`; synthetic automatic lvalue printed `D` and left
`004004=000104`. All halted at PC `001302`. Twenty-two host tests pass and verify
the fixed streams, oracle decoding, base-KA11-only words, 24 KB bounds,
bootstrap non-overlap, address scaling, KL11 addresses, and deterministic
deposits.

The first A attempt halted before SIMH serviced its queued console character.
It is preserved as failure evidence. The class-B project `emit` service now
polls TPS again after writing TPB so output completes before immediate HALT;
the five Thompson-derived operators were unchanged. Startup, `emit`, `stop`,
fixed placement, deposits, and transcripts are reconstruction/test scaffolding
(B/M), not documented original fragments or part of the final tape workflow.

Stage 3B remains: general threaded control, calls/returns, real frame creation,
arguments, and the other machinery required for a minimal representative B
program. Stage 3 as a whole is not complete.

Do **not** begin Stage 3B in the Stage 3A commit, or begin a PDP-11 backend,
cross-assembler, loader/tape format, arithmetic expansion, or `dc`. Do not
modify the existing PDP-7 compiler/runtime to support later stages.

## Resume here

Begin Stage 3B only in a new, separately scoped change. First investigate and
document the evidence boundary for general control, calls/returns, frame setup,
and arguments; do not extrapolate them from the proven 3A fragments. Extend the
smallest deterministic host/deposit tests needed for that gate while keeping
the oracle and deposits class M. Do not add KE11/EIS, arithmetic expansion, a
backend, cross-assembler, loader/tape format, or `dc`.
