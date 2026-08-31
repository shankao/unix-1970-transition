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

**Stage 1 — current:** characterize the existing PDP-7 B environment. The gate
is a checked-in, observed interface specification showing how representative B
source passes through the reconstructed PDP-7 compiler, its generated form,
the surviving PDP-7 interpreter/runtime, and execution. Stages 2–10 have not
started.

## Completed work

- **Stage 0 — complete.** `5e9221ed27fc16acee98914472e7c48452933004`
  imported the persistent PDP-7 host; `31ba389bae8f0ac9fa6391e0386a15450605f7cc`
  closed the static reproducibility capture. See `STATE.md` and
  `evidence/pdp7-import-manifest.tsv`.

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

## Current unknowns and next gate work

Stage 1 must identify the installed PDP-7 B compiler/runtime components and
their provenance, invocation, intermediate representation, operator contract,
and behavior for constants, storage, arithmetic, control flow, calls,
arguments, vectors, and external/library calls. Static audit and probe design
must precede the first project boot. Failures or divergent behavior are
evidence and must be recorded rather than repaired silently.

Do **not** begin a PDP-11 backend, cross-assembler, loader/tape format,
PDP-11 runtime, Stage 2 oracle, or `dc`; do not modify or boot the PDP-11; do
not modify the existing PDP-7 compiler/runtime merely to pass probes.

## Resume here

Start Stage 1A with a read-only inventory of B-related material under
`machines/pdp7`, compare the active and retained-reference trees by hash, and
write `docs/B-BASELINE.md` plus `evidence/pdp7-b-inventory.tsv`. Update this
file with material findings before designing or running probes.
