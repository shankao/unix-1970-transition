# Current Experimental State

This file records the starting point for repository work. Exact local paths and hashes still need to be captured from the machines.

## Chronological target

Late summer / pre-disk 1970 transition from PDP-7 UNIX development to a newly delivered PDP-11/20.

We intentionally do **not** jump directly to the November 1971 First Edition system.

## PDP-7

Role: functioning development host.

Known current characteristics:

- SIMH PDP-7
- 8K 18-bit words
- EAE enabled
- RB09 filesystem image
- PDP-7 UNIX restoration running
- custom user `shankao` exists (UID octal 16)
- B reconstruction available
- native assembler available
- `ed`, `roff`, shell, fork/background jobs explored
- PTP/PTR exist in the restoration environment; attachment state to be recorded before first project use

Important preservation rule: the PDP-7 machine is not disposable setup machinery. It is part of the experiment and must remain reproducible.

## PDP-11/20

Role: new diskless target machine.

Current visible enabled hardware:

```text
CPU     PDP-11/20, 24 KB
CLK     60 Hz, address 17777546-17777547, vector 100, BR6
TTI     address 17777560-17777563, vector 60, BR4
TTO     address 17777564-17777567, vector 64, BR4
PTR     address 17777550-17777553, vector 70, BR4; not attached
```

Known disabled/not present for this stage:

```text
no disk
no RK/RF/RL/RX
no Massbus
no tape drives
no networking
no ROM
no KE11
no UNIX V1 image
```

A 14-word DEC paper-tape bootstrap has been deposited but not executed:

```text
057744  016701
057746  000026
057750  012702
057752  000352
057754  005211
057756  105711
057760  100376
057762  116162
057764  000002
057766  057400
057770  005267
057772  177756
057774  000765
057776  177550
```

## To capture before Stage 1

- exact Open SIMH commit/version for both emulators;
- complete SIMH startup files;
- filesystem/disk image filenames and SHA-256 hashes;
- repository commits for the PDP-7 restoration/B reconstruction currently in use;
- host OS/tool versions relevant to reproducibility;
- current PDP-7 PTP/PTR state.

