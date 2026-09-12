# Stage 0 PDP-7

- Project state: reproducible imported PDP-7 development baseline, before
  Stage 1 B characterization
- Source commit: `5e9221ed27fc16acee98914472e7c48452933004`
- Original path: `machines/pdp7/pdp7-unix/build/image-shankao.fs`
- Source-checkpoint image SHA-256:
  `d1df123daf77d2c207972318a23a98176c9be4f4f10eeb8fe84328ac682fa490`
- Current experiential image SHA-256:
  `15eb6208c9820deef591f2f3568655bc163f374de4f281ceec0b14f9cef13e44`
- `boot.rim` SHA-256:
  `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2`

This is the first exact imported persistent project-host image. It retains the
existing `shankao` account and exploratory files. Stage 1 characterization
artifacts and all `as11` reconstruction work do not yet exist.

The current `pdp7.fs` contains intentional user changes made after its original
exact materialization; the source-checkpoint hash above preserves that
distinction. From this directory run `pdp7 pdp7.simh`, then connect a second
terminal with `telnet localhost 12345`.
