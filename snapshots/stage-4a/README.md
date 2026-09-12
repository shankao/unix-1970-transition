# Stage 4A PDP-7

- Project state: completed B two-pass I/O substrate
- Source commit: `1143e4de12138bd9a18c9afcf627038478b7991e`
- Original path: `machines/pdp7/pdp7-unix/build/image-shankao.fs`
- SHA-256: `ab6494ab9c3f786544533ff2cd9a054e639f64d8e5095eb4473bd4c965e6cab0`
- `boot.rim` SHA-256:
  `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2`

This checkpoint retains the `shankao`-owned rewind helper, B I/O test source,
deterministic input, build products, and result that proved mid-buffer,
cross-refill, and post-EOF rewind plus six-digit octal output. The Stage 4B
assembler-language and symbol engine do not yet exist.

From this directory run `pdp7 pdp7.simh`, then connect a second terminal with
`telnet localhost 12345`.
