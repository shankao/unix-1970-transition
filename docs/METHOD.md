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

Historical provenance and copyright license are separate dimensions. An
`A1 -> B` ancestry statement does not itself grant or identify redistribution
terms. Before copying, modifying, or closely adapting material, apply the
policy in [`../LICENSES/README.md`](../LICENSES/README.md) and record both its
source relationship and applicable license. Project-original material
normally uses `GPL-3.0-only`; imports and close derivatives retain their
applicable upstream notices.

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

## Historical-machine development record

`machines/pdp7` is the authoritative evolving host and normal work runs there
directly. A successful PDP-7 development substage normally checkpoints its
filesystem image, hash, and useful native artifacts in Git; in-progress image
changes are expected. Preserve meaningful sources, compiler/assembler output,
executables, inputs, and results rather than cleaning them merely because a
modern workflow calls them intermediate.

A development checkpoint and an experiential snapshot serve different needs.
Every passing PDP-7 development gate normally records the authoritative image;
selected states that expose a distinct, useful moment are additionally copied
as exact physical images under `eras/`. Snapshot provenance records the source
commit, original path, and SHA-256. The files remain ordinary, mutable Git
content rather than requiring an era-management or copy-on-boot layer. PDP-11
era organization is deferred until persistent tape/disk/machine combinations
provide concrete requirements.

For the currently understood PDP-7-only case, each selected era carries its
own README, recovered bootstrap, filesystem image, and direct SIMH configuration
so it can be used from that directory. This concrete duplication is intentional;
do not abstract it until repeated use reveals a real need. It does not prescribe
the later multi-machine/tape/disk layout.

Before relying extensively on a recovered tool or environment, inspect its
local source, documentation, and evidence; establish and verify one minimal
native behavior; then automate the observed procedure. Familiar later-Unix
names are not interface specifications. Cross-development tools likewise
follow bootstrap sufficiency: build the evidenced subset needed for the next
destination-machine capability rather than pursuing completeness as an end.

Native PDP-7 execution may be slow. That is not grounds to replace historical
computation with Python or another host tool. Optimize class-M orchestration:
keep persistent interactive SIMH sessions during discovery, reuse proven
flow-controlled transfer methods, avoid redundant work, and automate only once
the native procedure is understood.

## Migration-driven reconstruction

For the UNIX migration, begin with the actual local PDP-7 source and workload,
not with a desired cross-tool feature list. Select a responsibility, establish
the exact source variant and provenance, define the target semantics and
omissions, and only then derive missing assembler or machine requirements.
This keeps `as11`, threaded B, and `b11` in their evidenced role as bootstrap
scaffolding rather than allowing them to define the destination system.

Use the layered A1/A2/B/C/D source-lineage categories defined in
[`UNIX-MIGRATION.md`](UNIX-MIGRATION.md). They supplement rather than replace
the repository-wide A/B/C/D/M confidence labels and may overlap within one
file or routine. In particular, do not infer that a working file in a restored
source tree is an untouched contemporary original, or classify a whole file as
reconstruction because one local correction exists. Descendant V1 or later
material may constrain a reconstruction but does not become the 1970 target.
