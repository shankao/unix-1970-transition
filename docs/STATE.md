# Current Experimental State

This file records the starting point for repository work. Stage 0 capture is in
progress; the persistent PDP-7 host and static PDP-11 configuration are now
captured, but the remaining runtime-state gaps listed below keep the Stage 0
gate open.

## Chronological target

Late summer / pre-disk 1970 transition from PDP-7 UNIX development to a newly delivered PDP-11/20.

We intentionally do **not** jump directly to the November 1971 First Edition system.

## PDP-7

Role: functioning development host.

Machine roles:

- `../PDP-7` is the read-only pre-transition/reference machine. It is not a
  project working directory and must not be modified.
- `machines/pdp7` is the authoritative, persistent working PDP-7 host for this
  transition project. All future PDP-7 work starts there.

The complete local state was copied from `../PDP-7` on 2026-08-31 with
filenames and meaningful Unix modes preserved. Directories named `.git` were
excluded; no nested repository metadata is present in the import. The copy was
verified with a checksum-aware `rsync` dry run: 597 non-Git files in the source
and 597 files in the import, with no reported difference. The full size/mode/
SHA-256 inventory is `evidence/pdp7-import-manifest.tsv`.

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

The existing `shankao` account (UID octal 16), its filesystem contents, and
all exploratory files are intentionally retained. They are part of the frozen
pre-transition development state, not claims of original Bell Labs material.

### Imported restoration provenance

- Active tree: `machines/pdp7/pdp7-unix`, based on Git commit
  `e3ebcef20488b33eba8a7479cbd98b64e8af438b` on branch
  `add-user-directory-tool`. At import, `Makefile` and
  `build/unixv0.simh` were modified, and `Containerfile.simh`,
  `build/image-shankao.fs`, `build/pdp7`, `notes`, and `pr` were untracked.
- Retained reference tree: `machines/pdp7/pdp7-unix-copy`, based on Git commit
  `555eb30fc76b8fa29095d32eca9a43e9b1638288` on `master`. At import,
  `Makefile` was modified, and `Containerfile.simh` and `build/pdp7` were
  untracked.
- The active startup file is `machines/pdp7/pdp7-unix/build/unixv0.simh`.
  It configures an 8K PDP-7 with EAE, RB09, UNIX terminal translation,
  GRAPHICS-2 input on TCP port 12345, and attaches
  `build/image-shankao.fs`. It loads `build/boot.rim` at octal `010000`.
- Imported emulator: Open SIMH PDP-7 V4.0-0 Current, Git commit `aad53510`.

Key imported files:

| Path | Bytes | Mode | SHA-256 |
| --- | ---: | ---: | --- |
| `machines/pdp7/pdp7-unix/build/image-shankao.fs` | 4,096,000 | 0654 | `d1df123daf77d2c207972318a23a98176c9be4f4f10eeb8fe84328ac682fa490` |
| `machines/pdp7/pdp7-unix/build/image.fs` | 4,096,000 | 0654 | `8288b8df28eb713f149cfd7c4155b603159a95e8527edeae5caec50041d68633` |
| `machines/pdp7/pdp7-unix/build/boot.rim` | 69 | 0654 | `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2` |
| `machines/pdp7/pdp7-unix/build/unixv0.simh` | 533 | 0654 | `672c0f0bbe5be015e296285a207b91e746c2d50922f29666d489e2f12767ced6` |
| `machines/pdp7/pdp7-unix/build/pdp7` | 1,370,160 | 0755 | `6470b2066fa2847361c6f7377cf739c16b3408e2c54a3da854daf6e72ce587e7` |
| `machines/pdp7/pdp7-unix-copy/build/image.fs` | 4,096,000 | 0654 | `244b0876944fc60645f55ee9b5d3f293d0cca3d6267fc11d83c334286cacfd53` |
| `machines/pdp7/pdp7-unix-copy/build/boot.rim` | 69 | 0654 | `a69adf03a700058300501b2e4a74e732b344fd175e727c9a87c7c7b7132bd4f2` |
| `machines/pdp7/pdp7-unix-copy/build/unixv0.simh` | 492 | 0654 | `14ff89ea7ff0f457bb30c791bb082235a15e67d69d15856a041650fc054000c4` |

Filesystem images are expensive binary snapshots. A new image version is
committed only at a meaningful project milestone, with its hash and reason
recorded here or in a stage-specific evidence note. Routine PDP-7 sessions do
not each produce a committed image revision.

Important preservation rule: the PDP-7 machine is not disposable setup machinery. It is part of the experiment and must remain reproducible.

## PDP-11/20

Role: new diskless target machine.

The source machine remains at `../PDP-11` and was not modified or booted during
this capture. Its static startup configuration has been copied unchanged to
`machines/pdp11/pdp11.conf` so the repository does not depend on the sibling
path. The file is 522 bytes, mode 0664, SHA-256
`82cd40e79b453d384d503e4127425aa25052de557cf58bd65afb0602f9e933f0`.
The host `/usr/bin/pdp11` reports Open SIMH PDP-11 V4.0-0 Current, Git commit
`8a4b3752`; the binary is 2,730,056 bytes, SHA-256
`db667822b3c65ab2ea87eb59c17ddaf2369d32640d3a964994535b917a4d07da`.

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

Captured host/tool baseline: Ubuntu 26.04.1 LTS, Linux
`7.0.0-27-generic` x86-64, Git 2.53.0, Perl 5.40.1, and GCC 15.2.0.

Remaining Stage 0 gate items:

- Record the PDP-7 PTR/PTP runtime attachment state before the first project
  boot. The imported startup file contains no PTR/PTP attachment commands, but
  the prior interactive state was not queried and must not be guessed.
- Reconcile the PDP-11 transient state with the checked-in startup file.
  `machines/pdp11/pdp11.conf` disables CLK and does not deposit the recorded
  14-word bootstrap, while the observed state above has CLK enabled and those
  words in memory. A guarded later operation must capture or reproducibly
  encode that state without silently changing the intended machine.
- Record how the PDP-11 Open SIMH V4.0-0 binary at Git commit `8a4b3752`
  relates to the host package metadata, which reports Debian package
  `simh 3.8.1-6.3` despite the embedded V4.0 identification.

Until these items are resolved, the Stage 0 gate (recreate both machines from
repository documentation without relying on chat history) has not passed.
