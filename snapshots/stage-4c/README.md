# Stage 4C PDP-7

- Project state: completed bootstrap-sufficient KA11 encoding engine
- Source checkpoint: `b0379f3548c309d464d23dbcc5fb1178b19ccbe6`
- Original path: `machines/pdp7/pdp7-unix/build/image-shankao.fs`
- SHA-256: `d9a40b9ca80b1f9fa6623947faba1e0097ff8042d12d8e75236eb9b9081de245`
- `boot.rim` SHA-256:
  `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2`

This checkpoint retains the Stage 4A/4B substrate and the native Stage 4C
`as11` source, generated PDP-7 assembly, linked executable, fixtures, traces,
and capacity evidence. The two-pass language/symbol engine and bootstrap KA11
instruction encoding work. The final address/word object-map interface does
not yet exist. High artificial symbol pressure can exhaust ordinary-B memory;
Stage 4D must establish final capacity, safety margin, and clean exhaustion.

`b11`, paper-tape transfer, and PDP-11 UNIX do not yet exist.

From this directory run `pdp7 pdp7.simh`, then connect a second terminal with
`telnet localhost 12345`.
