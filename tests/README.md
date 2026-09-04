# Tests

Tests should focus on boundaries:

- B construct -> intermediate/threaded representation
- PDP-11 assembly -> words
- runtime operator -> machine behavior
- tape record -> decoded bytes/checksum
- PDP-7-produced tape -> PDP-11-loaded memory

End-to-end tests should preserve provenance and identify any modern instrumentation involved.

`test_stage3a.py` verifies the fixed class-M build products and the captured
bare-machine transcripts for the class-B threaded nucleus.
`test_stage3b.py` verifies control targets, frame/call layout, argument and
return placement, nesting, generated deposits, and the Stage 3B transcripts.
`test_stage4a.py` verifies the checked-in Stage 4A helper, fixture, runner
contract, and captured native evidence. It is host-only; the actual PDP-7 gate
is `python3 tools/run_stage4a.py --record`.
`test_stage4b.py` verifies fixed native trace hashes, compact-table/two-pass
source contracts, Stage 3 capacity demand, and absence of Stage 4C encoding.
Scanner, parser, expression, and symbol semantics execute only in PDP-7 B.
