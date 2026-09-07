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
source contracts, and Stage 3 capacity demand. Scanner, parser, expression,
and symbol semantics execute only in PDP-7 B.
`test_stage4c.py` checks the locally derived Stage 3 mnemonic inventory,
address/extension vectors, branch boundaries, oracle decoding, and that the
runner remains instrumentation rather than a host encoder. Actual encoding
continues to execute in B on the PDP-7.
`test_stage4c_capacity.py` validates the fixed capacity generator, exact
17-global/5-local Stage-3 shape, recorded pass/fail frontier, and oracle
decoding of the native Stage-3-shaped trace.
