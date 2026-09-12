# Stage 4B PDP-7

- Project state: completed `as11` language and symbol engine
- Source commit: `313ba822d1e962b4bba2360805717820db61a0c5`
- Original path: `machines/pdp7/pdp7-unix/build/image-shankao.fs`
- SHA-256: `3543d5a5e055072c9c99af0204a01479caa62b62442dc84b8c08d2631dad4c5a`
- `boot.rim` SHA-256:
  `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2`

This checkpoint retains Stage 4A support and the native `as11.b`, generated
PDP-7 assembly, linked executable, fixtures, and semantic results for the
two-pass scanner/parser, expressions, globals, and numeric locals. PDP-11
instruction encoding (Stage 4C) does not yet exist.

From this directory run `pdp7 pdp7.simh`, then connect a second terminal with
`telnet localhost 12345`.
