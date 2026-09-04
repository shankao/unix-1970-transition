# Stage 1 PDP-7

- Project state: completed PDP-7 B characterization
- Source commit: `9077f6a6a124682f22a0de79a5cbfd48416de0d3`
- Original path: `machines/pdp7/pdp7-unix/build/image-shankao.fs`
- SHA-256: `27799503d6f4a7067b25aeb081c5634c2f6c3bd28749bf6dcd71ff996e309027`

This image contains the native state left by Stage 1's B compiler/runtime
characterization. Ten final probe captures used `dmr` because of authentic
file ownership/linkage constraints; that caveat does not invalidate their
semantic evidence. The subsequent account-policy commit changed documentation
only and contains this same image blob. Stage 4 I/O and `as11` work do not yet
exist.
