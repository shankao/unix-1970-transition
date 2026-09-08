# KL11 polling input/output diagnostic

This is a modern class-M bare-machine diagnostic, not Unix kernel code.
`tests/pdp7-as11/kl11-poll.s` was transferred to the authoritative PDP-7 and
assembled there by the B-hosted `as11`. `native-trace.txt` is the resulting
`i`/`x`/`w` output; its SHA-256 matches the same trace extracted directly from
`pdp7-session.transcript.txt`.

`tools/run_kl11_poll.py` decodes the native instruction records with the
independent Stage-2 oracle, verifies the expected KL11 operands and scratch
data, and writes `artifacts/kl11-poll.simh` from those records. It contains no
instruction encoder. The generated artifact's 33 `dep` values are exactly the
33 native trace words.

The controlled PDP-11 run disabled PTY input echo, sent `A`, observed the
program's `A`, then sent `B` and observed the program's `B`. It halted at
`001076`. RAM examination showed:

```text
1100:   000101
1102:   000102
```

Thus reading the receiver buffer admitted a second input, and transmitter
READY cleared/reasserted sufficiently for two independently polled writes.
No interrupt-enable bit or vector was used.

The authoritative PDP-7 retains `dd/shankao/klpoll.s` (437 words) and
`klpoll.o` (320 words). Its final image SHA-256 is
`fa9294110e6e66eb5450aa600a5d52b0aba1e9d3d4f25223da67be582181b926`.
Read-only `fsck7` exits 0 with only the established inode-38/block-2987
self-revisit diagnostic.
