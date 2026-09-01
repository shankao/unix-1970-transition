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

**Stage 3 complete; both Stage 3A and Stage 3B gates passed.** The reconstructed
direct-threaded nucleus, control flow, frames, calls, arguments, void/value
returns, and nesting executed successfully on the bare PDP-11/20. **Stage 4 is
next and has not started.** Stages 5–10 have not started.

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
- **Stage 3B / overall Stage 3 — complete at this checkpoint.** Control,
  calls/frames, one/two arguments, void/value returns, and nested frames passed
  nine additional bare-machine tests. See `evidence/stage3b/`.

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

## Stage 3 result

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

Stage 3B adds class-B `f`, `tra`, `b4`, `mark`, `call`, `set`, automatic
rvalue `a`, archaeological `n11`, and `retv`. Calls follow the Stage 1 order:
function value, mark, left-to-right arguments, call. R2 temporarily identifies
the pending frame while caller R4 remains active for argument evaluation.
Frames contain old R4, saved R3, then argument/automatic words 2 onward.
Value return replaces saved-R3 word 1 with the result and advances R5 to word
2; void `n11` is materially unchanged and leaves R5 at word 1.

Actual results: E/F conditionals printed `E`/`F`; loop G printed `123` and
left its counter `000064`; synthetic unwind H printed `H`; one-argument I
printed `A`; two-argument add J printed `B` with slots 2/3 equal to
`000100`/`000002`; value return K printed `C`; nested L printed `D` with frame
chain `005006 -> 005000 -> 004000`; real void return M printed `V`. All halted
cleanly. Unchanged Stage 3A A/B/C/D scripts were rerun and passed. Thirty-one
host tests cover both stages, oracle decoding, frame/return placement,
transcripts, bounds, and deterministic deposits.

The detailed Thompson frame/register model is A evidence but postdates the
target. `n11` is B/C archaeological corroboration. Call entry, value return,
control fragments, and tests are class B/M reconstruction. No exact 1970 call
source is claimed. Stage 1 semantics and this convention do not conflict, but
the precise lost 1970 instruction sequence remains unknown.

One significant Stage 3B failure is retained: initial G stopped after `1`
because the first reconstructed `b4` destroyed CMP flags with CLR. Branching
before Boolean construction fixed it without changing evidenced fragments.

Do **not** begin Stage 4 arithmetic, a PDP-11 backend, cross-assembler,
loader/tape format, or `dc` in the Stage 3B commit. Do not modify the existing
PDP-7 compiler/runtime to support later stages.

## Resume here

Begin Stage 4 only in a new, separately scoped change. Audit the B arithmetic
contract against the base 11/20 and design software multiply,
division/remainder, and multi-bit-shift tests without KE11/EIS. Preserve all
Stage 3 A–M machine transcripts and host regressions. Do not begin the PDP-7
cross-assembler/backend, loader/tape format, or `dc`.
