# Stage 3A threaded-B nucleus

This directory contains a class **B** conservative reconstruction of the
strongly evidenced PDP-11 B direct-threaded nucleus. It is readable source and
not surviving late-1970 Bell Labs code. `core.s` closely transcribes the five
operator fragments printed in Ken Thompson's 7 January 1972 B manual.

`start`, `emit`, and `stop` are class-B project test support. The fixed memory
layout, Python encoder, generated deposits, SIMH execution, and transcripts are
class **M** instrumentation. They do not replace the eventual PDP-7 assembler
or paper-tape path. See `docs/PDP11-B-RUNTIME.md` for provenance and results.

Regenerate the modern artifacts and run host tests with:

```sh
python3 tools/build_stage3a.py
python3 -m unittest discover -v
```

Do not extend this Stage 3A source with control flow, calls, returns, or frame
creation; those are explicitly gated to Stage 3B.

Stage 3B is kept separately readable in `control-call.s`; its call entry and
value-return sequences are class-B inference, while its `n11` body closely
retains the cited archaeological reconstruction.
