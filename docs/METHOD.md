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
- recovered original filesystem material.

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

Host-side tools, tests, converters, scripts, CI, and emulator automation. These
are allowed and encouraged for reliability, but must be labelled when they
take part in the historical run being claimed.

## Source hierarchy

Prefer, in order:

1. contemporary original material;
2. primary participant accounts;
3. recovered binaries/listings and archaeological analysis;
4. high-quality later technical histories;
5. conservative inference;
6. modern analogy only as a last resort.

Conflicting sources are recorded rather than silently forced into agreement.

Later surviving Unix source may constrain a reconstruction as descendant
evidence, but must not silently be projected backward as 1970 fact.

## Reproducibility rule

A chat transcript is never the canonical record of a technical state. Once a fact affects the reconstruction, it belongs in this repository as one of:

- machine configuration;
- source note;
- decision record;
- test case;
- metadata for generated files.

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

## Outcome-based milestone completion

Every meaningful R/B/U parent milestone has a documented **Done when /
observable outcome**. Its component checkboxes describe necessary research or
implementation pieces; checking all of them is not by itself sufficient to
complete the parent. The parent is complete only after its outcome is reviewed
and demonstrated.

For implementation milestones, acceptance test programs must exercise the
actual target system. Modern runners and verification remain allowed, but a
host-side replacement for the system or target computation cannot satisfy the
outcome. Research milestones instead finish when they record the evidence,
remaining uncertainties, and implementation limits clearly enough to proceed;
they do not need synthetic execution tests merely for symmetry.

## Proven reconstruction workflow

Stages 0–3 established a working method for the remaining project:

1. Investigate public and historical evidence before implementation, unless
   the relevant investigation is already recorded in the repository.
2. Track historical confidence separately from technical feasibility. Code
   that works is not thereby authentic.
3. Build independent test/oracle layers before combining uncertain systems.
4. Prove dependencies in the order that working programs require them.
   Compiler, assembler, transport, loader, and runtime remain separate even
   when the final workflow connects them. A dependency may cross a U2/U3/U4
   accounting boundary; those groups do not prescribe coding order.
5. Preserve failures when they reveal a boundary; record the diagnosis and do
   not let later success erase informative evidence.
6. Modern instrumentation is acceptable for reconstruction and testing, but
   it must not perform the historical computation being claimed. Host control
   may remain M only when it does not create or alter the target program, tape,
   or other historical-side output.
7. Prefer a documented contemporary substitute to an invented undocumented
   mechanism when exact practice is lost, and label that substitute C.
8. Never promote descendant, binary-derived, or reconstructed code into
   original-source status merely because its behavior agrees.

## Code-generation and transport provenance

A target program or file has at least two independent provenance questions:

- **Code-generation provenance:** did the reconstructed historical-side tools
  genuinely produce the target words?
- **Transport provenance:** did those words reach target memory through the
  claimed historical or conservatively reconstructed transfer mechanism?

Direct SIMH deposit of exact PDP-7-produced words proves the first and remains
a valid fast development method; it does not prove the second. Historical
acceptance requires the emulated PDP-11 to execute the selected loader and
consume the tape through its reader. Modern automation may set switches,
deposit the small bootstrap, attach media, start machines, drive consoles, and
verify memory. The rule is: **reconstruct historical mechanisms, not historical
operator tedium.** Direct deposits and paper-tape loading coexist; do not
impose the slower method on every inner regression once it has been proven.

### Preserve historical development cost

Modern shortcuts may shorten debugging, but they must not remove historical
costs in a way that changes what we decide to build next.

Use the two loading methods in three different situations:

1. For a very small debug check or regression, direct deposit of exact
   PDP-7-produced words is fine.
2. For a substantial integrated change, use fast deposits while debugging if
   useful. Before that program becomes the basis for choosing the next change,
   produce it with the reconstructed PDP-7-side tools as applicable and load it
   through paper tape. Record the target word or byte count, tape byte count,
   and approximate period transfer cost.
3. For a historical or public acceptance test, use the paper-tape reader,
   bootstrap, and loader required by that test.

Contemporary DEC documentation provides scale, not proof of Bell Labs'
particular equipment: a PC11 high-speed reader ran at about 300 characters per
second, its punch at about 50 characters per second, and Model 33 ASR tape
operation at about 10 characters per second. Use these rates to judge design
cost; do not delay the emulator to reproduce wall-clock time. The exact Bell
Labs reader, punch, loader, and tape format remain unknown. See
[`SOURCES.md`](SOURCES.md).

Ask: **Would this still be the sensible next change if every substantial new
PDP-11 image had to be assembled on the PDP-7 and transferred by paper tape?**
If not, the fast method is distorting the reconstruction.

## Historical-machine development record

`machines/pdp7` is the authoritative evolving host and normal work runs there
directly. A successful PDP-7 development substage normally checkpoints its
filesystem image, hash, and useful native files and results in Git.
In-progress image changes are expected. Preserve meaningful sources,
compiler/assembler output, executables, inputs, and results rather than
cleaning them merely because a modern workflow calls them intermediate.

A development checkpoint and a historical era serve different needs. Every
passing PDP-7 development gate normally records the authoritative image;
selected exact project states live under `snapshots/` with source commit, path,
and hash provenance. They answer what this reconstruction had established.

`eras/` instead answers what a person might plausibly have interacted with
during historical-system evolution. Eras are selected for the capabilities
they show and need not correspond to dates or boundaries Bell Labs recognized.
Eras are living reconstructions: correct a known historical error when evidence
improves, record why and with what confidence, and rely on Git, evidence, and
snapshots to retain prior project results. Runnability does not raise an
evidence class.

Every era carries a concise `ERA.md` and, where practical, a direct emulator
command plus concrete interaction. Human replay complements automated
acceptance; neither substitutes for the other. Ordinary files and small
duplicated media remain preferable to an era manager or copy-on-boot
abstraction.

The public journey is not a gallery of engineering checkpoints. Git preserves
how our reconstruction evolved; `snapshots/`, tests, evidence, and contracts
retain selected project states and their technical foundation. Public eras
present our **current** historical model, not an obligation to retain a weaker
presentation because an earlier commit used it.

Create a public state only when it gives a person a tangible, historically
meaningful new capability and improves the journey. R/B/U completion alone
does not justify one. Prefer a few understandable experiences to a state for
every implementation increment; assembler availability and tape production
can be explored within one cross-development state. Success words and
diagnostics remain useful evidence, but are not themselves the public story.

**Automate repetition that teaches nothing. Preserve constraints and
mechanisms that explain the history.** For example, automate front-panel
entry and tape changes while retaining native production, PTR reading, and
actual loader execution. State clearly any difference between the automated
test and the steps a visitor can run.

Before relying extensively on a recovered tool or environment, inspect its
local source, documentation, and evidence; establish and verify one minimal
native behavior; then automate the observed procedure. Familiar later-Unix
names are not interface specifications. Cross-development tools likewise
follow bootstrap sufficiency: build the evidenced subset needed for the next
destination-machine capability rather than pursuing completeness as an end.

Native PDP-7 execution may be slow. That is not grounds to replace historical
computation with Python or another host tool. Run class-M tools efficiently:
keep interactive SIMH sessions open during discovery, reuse proven
flow-controlled transfer methods, avoid redundant work, and automate only once
the native procedure is understood.

## Migration-driven reconstruction

For the UNIX migration, begin with the actual local PDP-7 source and workload,
not with a desired cross-tool feature list. Select a responsibility, establish
the exact source variant and provenance, define the target semantics and
omissions, and only then derive missing assembler or machine requirements.
This keeps `as11`, threaded B, and `b11` in their evidenced role as bootstrap
tools rather than allowing them to define the destination system.

Filesystem, process, and command work should grow together when a working
program requires it. Do not finish a complete subsystem merely because its
roadmap number comes first. Build the first working file, use a small command
such as `cat` to exercise it, then add process loading, the shell, and the
remaining file operations as actual use demands them. This is a reconstruction
method, not a claim about Bell Labs' exact implementation order.

Use the layered A1/A2/B/C/D source-lineage categories defined in
[`UNIX-MIGRATION.md`](UNIX-MIGRATION.md). They supplement rather than replace
the repository-wide A/B/C/D/M confidence labels and may overlap within one
file or routine. In particular, do not infer that a working file in a restored
source tree is an untouched contemporary original, or classify a whole file as
reconstruction because one local correction exists. Descendant V1 or later
material may constrain a reconstruction but does not become the 1970 target.
