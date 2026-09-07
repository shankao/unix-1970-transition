# Stage 4C capacity characterization

This focused follow-up does not complete Stage 4C or change the encoder. It
measures the ordinary-B collision recorded in `evidence/stage4c/` using the
already-installed PDP-7 `a.out` as `shankao`.

`capacity-matrix.tsv` is the consolidated result. Exact traces pass through
38 globals/10 numeric-local definitions. At 39 globals, zero locals happens
to pass, but one or more locals cause `e 000051 ph` after partial correct
pass-2 output. The edge case is therefore not a safe capacity. The previous
48/10 Stage 4B fixture produces an empty output file.

The Stage-3-shaped fixture uses all 14 Stage 3 mnemonics, realistic operands,
17 globals, and five numeric-label definitions. It passes with a 1,249-byte
native trace; every instruction record decodes through the Stage 2 oracle.
Its static stack-label-to-global separation is 160 PDP-7 words, 105 more than
the narrowest representative passing case (38/10, 55 words).

The `capacity-NN-NN.tsv`, corresponding transcripts, and image files record
the successful bounded runner invocations. The initial long invocation was
externally terminated after recording valid 17/5 through 40/5 output files;
later bounded invocations resumed without rebuilding or retransmitting
`as11`.

The original long host process unexpectedly continued after its execution
session appeared orphaned and overlapped the preliminary 04–07 and 10–13
bounded runs. Those files are retained as orchestration evidence, but the
reported safe frontier relies on the later non-overlapping 15–18, 18–20, and
20–21 runs. The Stage-3-shaped fixture was rerun afterward in a verified sole
SIMH process; its final transcript and hash replace the overlapped preliminary
run for the gate evidence. Final `fsck7` validation passed.

The bounded-run TSVs used `017160` (the first post-sentinel address) for their
preliminary gap column. The consolidated `capacity-matrix.tsv` uses the exact
`bi.s` `stack`/`sp` base at `017157`, so its separation values are one word
larger and are authoritative.

This is a capacity regression, not loss of Stage 4B language semantics:
fixtures below the boundary exercise the same assignments, labels, numeric
locals, expressions, statement separators, two-pass rewind, and trace output
and match exactly. Stage 4C remains OPEN pending a guarded capacity decision
or further compacting.
