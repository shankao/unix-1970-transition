# Historical Method and Provenance Policy

## Principle

This project is an experimental reconstruction, not a claim to have recovered lost Bell Labs source.

Historical plausibility matters, but plausibility is not evidence. Every nontrivial component and claim must be traceable to evidence or explicitly marked as reconstruction/substitution.

## Provenance labels

### A — Authentic surviving material

Examples:

- scanned original source/listings;
- surviving binaries whose origin is established;
- contemporary DEC manuals;
- primary historical accounts by participants;
- recovered original filesystem artifacts.

Class A does **not** mean "the file is unmodified in our tree" unless that is separately established.

### B — Conservative reconstruction

New implementation of a lost component using the strongest available evidence. A B component should document:

- what historical component it is intended to reproduce;
- which sources constrain its behavior/interface;
- which design decisions remain inferred;
- how it differs from later known implementations.

### C — Historically close substitute

A real period or near-period component used where Bell Labs' exact counterpart is undocumented or unavailable.

Example candidate: a documented contemporary DEC paper-tape loading format if Bell Labs' exact 1970 tape format remains unknown.

A class C substitute must never silently turn into a claim about what Bell Labs used.

### D — Unknown / unrecoverable

Use this explicitly. Unknown is a valid result.

### M — Modern instrumentation/convenience

Host-side tools, tests, converters, scripts, CI, and emulator automation. These are allowed and encouraged for reliability, provided they are not inserted into the final historical execution path without being labelled.

## Source hierarchy

Prefer, in order:

1. contemporary original artifacts;
2. primary participant accounts;
3. recovered binaries/listings and archaeological analysis;
4. high-quality later technical histories;
5. conservative inference;
6. modern analogy only as a last resort.

Conflicting sources are recorded rather than silently reconciled.

## Reproducibility rule

A chat transcript is never the canonical record of a technical state. Once a fact affects the reconstruction, it belongs in this repository as one of:

- machine configuration;
- source note;
- decision record;
- test fixture;
- generated artifact metadata.

## Imported code

Do not copy code from external historical/restoration repositories until its licensing and provenance have been checked.

If imported, retain:

- upstream URL;
- commit/revision;
- original path;
- license/copyright information;
- cryptographic hash of imported source where practical;
- local modifications as separate commits or patches.

## Failure policy

When a stage fails:

1. reduce it to the smallest reproducible boundary;
2. determine whether the failure is historical assumption, reconstruction code, emulator behavior, or modern tooling;
3. update the decision/evidence record;
4. fix that boundary before proceeding.

Do not compensate for failure by silently enabling later hardware/software or importing a later implementation.

## Proven reconstruction workflow

Stages 0–3 established a working method for the remaining project:

1. Investigate public and historical evidence before implementation, unless
   the relevant investigation is already recorded in the repository.
2. Track historical confidence separately from technical feasibility. Code
   that works is not thereby authentic.
3. Build independent test/oracle layers before combining uncertain systems.
4. Prove one dependency at a time. Compiler, assembler, transport, loader,
   and runtime remain separate even when the final workflow connects them.
5. Preserve failures when they reveal a boundary; record the diagnosis and do
   not let later success erase informative evidence.
6. Modern instrumentation is acceptable for reconstruction and testing, but
   it must disappear from the final claimed historical data path. Coordination
   may remain M only when it does not create or alter the historical artifact.
7. Prefer a documented contemporary substitute to an invented undocumented
   mechanism when exact practice is lost, and label that substitute C.
8. Never promote descendant, binary-derived, or reconstructed code into
   original-source status merely because its behavior agrees.
