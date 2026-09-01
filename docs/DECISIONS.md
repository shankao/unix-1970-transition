# Decision Log

Short append-only project decisions. Reverse a decision by adding a new entry rather than rewriting history.

## D0001 — Historical honesty over exact-looking simulation

**Status:** accepted

The project is an exercise in using surviving parts in a way that fits historical accounts, while clearly stating what is original, reconstructed, substituted, or unknown. We will not claim exact recovery where source has been lost.

## D0002 — Produce a reusable public project, not only an emulator session

**Status:** accepted

The repository, documentation, tests, generated artifacts, and reproducible workflow are first-class deliverables. Chat instructions alone are not considered project output.

## D0003 — Dependency-gated implementation

**Status:** accepted

Do not begin later stages merely because the next emulator command is available. Each roadmap stage has an explicit gate intended to expose architectural failures early.

## D0004 — Modern tooling is allowed as instrumentation

**Status:** accepted

Modern host-side tests, scripts, converters, CI, and verification tools are encouraged during reconstruction. They must be class M and excluded from the final historical code-generation path unless explicitly documented.

## D0005 — No silent optional PDP-11 hardware

**Status:** accepted

The diskless PDP-11/20 remains configured without KE11 unless historical evidence justifies enabling it. Missing arithmetic operations should initially be handled in software or by restricting the supported B subset.

## D0006 — Bell Labs paper-tape encoding remains unresolved

**Status:** accepted

Paper-tape transfer is historically attested, but the exact Bell Labs record/loading format is not yet established. A contemporary DEC format may be used as class C if required, but must not be described as the Bell Labs format without evidence.

## D0007 — Repository-wide licensing deferred

**Status:** accepted

Do not add a blanket repository license until we decide how newly written code, documentation, imported PDP-7 material, reconstructed B material, and generated artifacts will be separated. Imported source must retain upstream licensing/provenance.

## D0008 — Split the threaded-B runtime gate into Stage 3A and Stage 3B

**Status:** accepted

Stage 3A is limited to the strongly evidenced R3/R4/R5 direct-threaded nucleus
and documented `c`, `x`, `va`, `b12`, and `b1` semantics. The reconstruction
is class B because Thompson's detailed manual is from January 1972 and the
exact late-1970 source is lost. Control flow, calls, returns, real frame setup,
arguments, and the remaining minimal execution machinery are a separate Stage
3B gate; Stage 3A success must not be described as completion of all Stage 3.

## D0009 — Stage 3B pending-frame and return-value convention

**Status:** accepted

Reconstructed argument-bearing calls follow the observed Stage 1 ordering:
function value, mark, left-to-right arguments, call. `mark` reserves
`[old R4, callee]` at R5 and records the pending frame in temporary R2 without
changing R4; `call` replaces the callee word with saved R3 and activates R4.
Arguments occupy frame words 2 onward. Value return replaces saved-R3 word 1
with the result and leaves R5 at word 2; void `n11` leaves R5 at word 1. This
is class B inference consistent with class-A frame semantics, Stage 1 output,
and B/C archaeology, not recovered late-1970 source.

## D0010 — Persistent project PDP-7 and development identity

**Status:** accepted

`machines/pdp7` is the authoritative persistent working host; `../PDP-7` is a
read-only pre-transition reference. Project work normally uses `shankao` and
does not change historical accounts or hard-linked authentic files merely to
bypass permissions. Working copies and generated artifacts remain
distinguishable from authentic, reconstructed, and restored originals.

## D0011 — Separate assembler, compiler, and tape transport

**Status:** accepted

Stage 4 reconstructs `as11`, a B-written PDP-11 assembler running on the
PDP-7. Stage 5 separately reconstructs `b11`, which emits a readable PDP-11
threaded assembly/representation for `as11`. Paper-tape construction and
loading are Stage 7 transport concerns and belong to neither tool. This lets
Stage 6 verify compiler and assembler with class-M loading before introducing
the historically uncertain tape boundary.

## D0012 — Contemporary DEC loader only as a labelled fallback

**Status:** accepted

Physical PDP-7-to-PDP-11 paper-tape transfer is attested, but its exact Bell
Labs format remains unknown. DEC Absolute Binary/Absolute Loader machinery
may be selected later as class C if no stronger evidence emerges. Selection
would establish a contemporary substitute, not evidence that Bell Labs used
that convention.

## D0013 — Repository endpoint is the December 1970 disk transition

**Status:** accepted

The required completion gate is a reproducible first disk-backed PDP-11 UNIX
environment consistent with surviving evidence for the December 1970 disk
arrival. Core-only/RAM-filesystem UNIX and disk migration are explicit
high-risk stages. Later 1971 development toward First Edition is outside this
repository's required scope and may be continued separately.
