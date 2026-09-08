# Stage-3 gold round trip

This is class-M integration evidence. `native-trace.txt` was emitted by the
PDP-7 B `as11` from `tests/pdp7-as11/stage3b-gold.s`. The host runner parses
only `i`/`x`/`w` word records (plus metadata), rejects malformed or duplicate
addresses, and verifies the native map against the independent Stage-2-backed
Stage-3B test-L manifest. It does not encode or replace instructions.

`test-l.simh` deposits the 110 parsed native words verbatim. The PDP-11
transcript records the expected visible result `D`. `gold.s` and `gold.o`
remain as useful native artifacts in `dd/shankao` on the authoritative PDP-7
image.

Development CPU timing for the same Stage-4C build-only command was 533.09 s
with `set throttle 400K` and 87.76 s with `set nothrottle`. The terminal
transfer delay remained 80 ms per character.

Final validation for this checkpoint:

- Stage 4A native regression: PASS;
- Stage 4B functional language/negative regression: PASS;
- Stage 4C functional encoding/rejection regression: PASS;
- host tests: 72 PASS;
- `fsck7`: exit 0, with only the known inode-38/block-2987 self-revisit;
- final authoritative PDP-7 image SHA-256:
  `5ce0c014a19f25242893dcc3f0ab7a654a819d263732b50253332dbaf4e7c3f2`.
