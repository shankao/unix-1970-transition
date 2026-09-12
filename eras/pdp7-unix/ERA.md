# Late PDP-7 Unix

## Historical hypothesis

This era represents a usable late PDP-7 Unix environment before reconstructed
PDP-11 cross-development tools dominate the experience. It is a
capability-based slice, not a claim for an exact date or Bell Labs milestone.

## Evidence / provenance

The boot path, Unix filesystem, commands, and historical accounts are class A
or restored derivatives with mixed provenance described in `LICENSES/README.md`.
The runnable image is the project's earliest imported persistent baseline
(formerly the Stage 0 project snapshot), so its `shankao` account and
exploratory files are restoration/project additions rather than untouched
historical state. Treat the assembled experience as a conservative model, not
a recovered point-in-time disk.

## What exists

A self-contained PDP-7 configuration, bootstrap, RB09 filesystem, command
environment, and restored source tree. PDP-11 cross-development acceptance is
not represented by this slice. The selected `pdp7.fs` SHA-256 is
`15eb6208c9820deef591f2f3568655bc163f374de4f281ceec0b14f9cef13e44`.

## Run it

From this directory:

```sh
pdp7 pdp7.simh
```

The emulator boots Unix. Its GRAPHICS-2 terminal also listens on TCP port
12345; `telnet localhost 12345` may be used from another terminal.

## Try this

At `login:`, use `shankao` / `shankao`, then run `ls`.

## Expected result

The restored shell prints the account's files and returns to its `@ ` prompt.

## Acceptance / regression

The documented launch was exercised directly during era creation. `python3 -m
unittest tests.test_eras` guards the era/snapshot structure. Stage 0 evidence
remains under `evidence/`; the exact original project checkpoint remains in
`snapshots/stage-0/`.

## Known uncertainties

This image combines surviving/restored Unix with project account state.
Its selection as a late-PDP-7 experiential baseline is reconstructive and does
not establish exact historical disk contents or chronology.
