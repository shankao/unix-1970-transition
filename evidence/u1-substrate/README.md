# U1 bare-machine substrate evidence

These class-M captures prove the remaining U1 checkboxes using PDP-11 words
emitted by native PDP-7 `as11`.

- `interrupt-native-trace.txt` and `ram-native-trace.txt` are the native
  `i`/`x`/`w` records.
- `interrupt-pdp11.transcript.txt` records two real KL11 receive interrupts,
  interrupt-driven transmission, RTI return, and diagnostic TRAP return.
- `ram-pdp11.transcript.txt` records allocation, exhaustion, free/reuse, and
  a 512-byte RAM-block write/read round trip.
- `pdp7-session.transcript.txt` is the latest native assembly session;
  `image-state.txt` records its filesystem-image state.

The host harness parses, verifies, deposits, drives SIMH, and inspects results.
It does not encode or replace PDP-11 instructions.
