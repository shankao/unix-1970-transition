# PDP-7 development snapshots

These directories preserve directly explorable PDP-7 filesystem images from
distinct points in the reconstruction. They are ordinary tracked files,
materialized once from exact Git blobs; using one does not require checking out
an old commit. The configuration under `machines/pdp7` remains the reference
for running the PDP-7.

The images are not immutable museum objects. A user may boot and change one;
normal Git usage such as `git restore eras/stage-4b/pdp7.fs` restores its
recorded bytes. Each successful PDP-7 development gate still checkpoints the
authoritative image under `machines/pdp7`; only machine states that usefully
show a distinct part of the development journey need a featured snapshot here.

This initial layout covers PDP-7 filesystem images only. Representation of
later PDP-11 RAM, tape, disk, and paired-machine states is deliberately deferred
until those states have real operational requirements.
