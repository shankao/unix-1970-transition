# Stage 4C open-gate evidence

Stage 4C is **OPEN**, not complete. All native work here ran as `shankao` on
the authoritative `machines/pdp7` host. The PDP-11 was not booted.

The native encoder produced the exact `enc.s.out` trace: 30 instructions plus
extensions covering all eight modes, PC-special forms, byte extensions,
dual-extension ordering, branch boundaries, JMP/JSR/RTS, and every mnemonic
used by Stage 3. The trace agrees with the independent Stage 2 oracle.
`pos.s.out` preserves the passing ordinary Stage 4B semantic regression, and
the 18 `b*.s.out` files preserve the expected rejection traces.

The gate remains open because the 604-byte `stage4b-substantial.s` case (48
globals and 10 numeric-local definitions) created an empty output file. The
final transcript and `failure-latest.txt` record that result. The 3,696-word
linked program starts its B stack immediately below the maximum high-memory
symbol arena, leaving only five words; this is a resource collision, not an
encoding discrepancy.

Earlier informative iterations found a 4,958-word link overflow and then
4,021/3,982/3,943-word layouts that linked but collided with runtime stack or
I/O storage. The final source removes static symbol arrays, packs symbol state
into unused name bits, and reduces the linked result to 3,696 words, but does
not yet satisfy the established scale gate. No native Stage 4C `readme` was
installed and no `eras/stage-4c` snapshot was created because those are PASS
artifacts.

Files:

- `stage3-inventory.txt`: inventory derived from local Stage 3 sources.
- `enc.s.out`, `pos.s.out`, `b*.s.out`: successful native traces.
- `session.transcript.txt`: final native build/run transcript.
- `native-stat.txt`: native `as11.b`, `as11.s`, and `a.out` sizes.
- `image-state.txt`: runner image hashes and repository state.
- `failure-latest.txt`: final maximum-capacity failure.
- `checkpoint-open.txt`: image/integrity/resource checkpoint summary.
