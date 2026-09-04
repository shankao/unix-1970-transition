# Stage 4B evidence

All `*.s.out` files were created by the B program running as `shankao` on
authoritative `machines/pdp7`. `pos.s.out`, `large.s.out`, and empty output are
successful traces; the other thirteen are expected diagnostics. The class-M
runner captures/hash-checks them but implements no language semantics.

- `session.transcript.txt`: final complete native build and 16-fixture run.
- `native-stat.txt`: source, generated assembly, and executable word sizes.
- `image-state.txt`: runner pre/post hashes and Git state.
- `diagnostic-failures.txt`: informative failures/interruption record.
- `checkpoint.txt`: final image and integrity interpretation.

Recovered PDP-7 `ed` behavior learned here is in `docs/PDP7-TOOLS.md`.
