# UNIX 1970 Transition Reconstruction

A historically grounded reconstruction of the transition from PDP-7 UNIX to the first diskless PDP-11/20 work at Bell Labs in 1970.

The project is not an attempt to claim that lost source has been recovered. Its purpose is to use surviving code, contemporary documentation, later archaeological reconstructions, and explicitly labelled new reconstruction work to reproduce the development path described by Dennis Ritchie, Ken Thompson, and other primary sources as faithfully as the evidence allows.

## Target experience

The central experiment is:

```text
PDP-7 UNIX development host
        |
        | B-hosted PDP-11 cross-development
        v
PDP-11 object / paper tape
        |
        | simulated physical transfer
        v
bare 24 KB PDP-11/20
        |
        +-- no disk initially
        +-- console + paper-tape reader
        +-- standalone threaded-B programs
        +-- eventually a reconstructed early dc-like program
```

The goal is not merely to make PDP-11 code run. The goal is to reproduce the *workflow* in a form where every historical, reconstructed, substituted, and modern-convenience component is identifiable.

## Historical basis

Primary accounts establish that:

- the PDP-11 processor arrived before its disk;
- B programs were moved to the PDP-11 using threaded code;
- PDP-11 operator fragments and a simple assembler were written for this purpose;
- the PDP-11 assembler was written in B and run on the PDP-7;
- paper tape was physically carried from the PDP-7 to the PDP-11;
- `dc` was among the earliest interesting programs to run on the PDP-11 before the operating system was usable there.

See [`docs/SOURCES.md`](docs/SOURCES.md) for sources and claim-level notes.

## Provenance classes

Every substantial component must be classified:

- **A — Authentic surviving material**: original source, binary, scan, listing, manual, or other contemporary artifact.
- **B — Conservative reconstruction**: new work intended to reproduce a lost component from surviving evidence.
- **C — Historically close substitute**: contemporary or near-contemporary machinery used where Bell Labs' exact implementation is unknown.
- **D — Unrecoverable / unknown**: a component or behavior for which evidence is currently insufficient.
- **M — Modern instrumentation/convenience**: test harnesses, converters, scripts, host-side verification tools, CI, and emulator automation. These may support development but must not be mistaken for part of the historical execution path.

## Current status

Planning and evidence audit are complete enough to begin implementation, but no reconstructed cross-toolchain has yet been written.

The current machines are intentionally frozen at the transition point:

- PDP-7: working late-1970-style UNIX development host.
- PDP-11/20: 24 KB, console and clock, PC11 paper-tape reader enabled, no disk, no KE11, no UNIX image.
- A 14-word contemporary DEC paper-tape bootstrap has been deposited at the top of PDP-11 memory but has not been executed.

See [`docs/STATE.md`](docs/STATE.md).

## Roadmap

The implementation is dependency-gated. We do not proceed to the next stage merely because the previous stage produced output.

1. Characterize the working PDP-7 B environment.
2. Build modern verification tooling.
3. Reconstruct a minimal standalone PDP-11 threaded-B runtime.
4. Resolve PDP-11/20 arithmetic constraints without silently adding KE11.
5. Reconstruct the B-written PDP-11 assembler on the PDP-7.
6. Reconstruct the PDP-7-hosted B-to-PDP-11 backend.
7. Establish a general paper-tape loading format and clearly classify any substitute.
8. Prove the full B-source -> PDP-7 -> tape -> bare PDP-11 loop.
9. Build a small calculator as a systems test.
10. Attempt a historically grounded `dc` reconstruction.

The full gates and failure conditions are in [`docs/PLAN.md`](docs/PLAN.md).

## Repository layout

```text
docs/       project plan, historical method, machine state, decisions
evidence/   claim matrices, notes, hashes/metadata for examined artifacts
src/pdp7/   code intended to execute on the PDP-7
src/pdp11/  code intended to execute on the PDP-11
tools/      modern host-side verification and build tooling
tests/      regression vectors and end-to-end tests
artifacts/  generated tape images, listings, dumps; normally not authoritative
LICENSES/   provenance and licensing notes for imported material
codex/      handoffs/instructions for Codex sessions
```

## Project rule

A successful output is not enough. For every stage we must be able to answer:

1. What exactly produced this artifact?
2. Which parts are original, reconstructed, substituted, or modern?
3. What historical evidence justifies the interface between those parts?
4. Can the result be reproduced from the repository?

