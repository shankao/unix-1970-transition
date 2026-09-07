# PDP-7 development snapshots

These directories preserve directly explorable PDP-7 machine states from
distinct points in the reconstruction. Each current PDP-7-only era is a
self-contained directory with `README.md`, `boot.rim`, `pdp7.fs`, and
`pdp7.simh`; using one does not require checking out an old commit or referring
to `machines/pdp7`.

From the selected era directory, start the locally installed SIMH PDP-7 with:

```sh
pdp7 pdp7.simh
```

The configuration listens for the PDP-7 GRAPHICS-2 terminal on TCP port 12345.
In a second terminal connect with `telnet localhost 12345`, then use the PDP-7
login prompt. Exit or disconnect that terminal before ending SIMH. Only one era
can use port 12345 at a time without an intentional configuration change.

`boot.rim` is the recovered project bootstrap from
`machines/pdp7/pdp7-unix/build/boot.rim` (SHA-256
`a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2`).
The era-local configuration attaches only its own `pdp7.fs`, leaves paper tape
unattached, loads the bootstrap at octal `010000`, and runs it.

Current PDP-7 snapshots are `stage-0`, `stage-1`, `stage-4a`, `stage-4b`, and
`stage-4c`.

The images are not immutable museum objects. A user may boot and change one;
normal Git usage such as `git restore eras/stage-4b/pdp7.fs` restores its
recorded bytes. Each successful PDP-7 development gate still checkpoints the
authoritative image under `machines/pdp7`; only machine states that usefully
show a distinct part of the development journey need a featured snapshot here.

This layout covers PDP-7-only eras while that simple arrangement is sufficient.
Representation of
later PDP-11 RAM, tape, disk, and paired-machine states is deliberately deferred
until those states have real operational requirements.
