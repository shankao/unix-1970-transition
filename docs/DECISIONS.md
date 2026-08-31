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

