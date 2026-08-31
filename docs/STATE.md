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
- PTR is device 01 and PTP is device 02; both are enabled and unattached at the
  start of a fresh emulator process

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
- A configuration-only query of the imported emulator (no startup file, image
  attachment, bootstrap load, or `go`) reported `PTR devno=01, not attached`
  and `PTP devno=02, not attached`. The active startup file now explicitly
  enables both devices and contains no attachment command for either, making
  that initial state deterministic for a fresh project session. The updated
  file is 663 bytes, repository mode 0644, SHA-256
  `4147344078e9b91612dff6b8134a9afae009e2f70602893f697b134f41d24bd0`.
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

The table and full manifest describe the immutable initial import in commit
`5e9221ed27fc16acee98914472e7c48452933004`. Subsequent project configuration
changes, such as making PTR/PTP enablement explicit, are ordinary reviewed Git
changes and do not rewrite the import manifest.

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

### Observed former live session

The following was observed volatile runtime state in the previous PDP-11 SIMH
session. That session was subsequently exited. The PTR observation was:

```text
PTR     address=17777550-17777553, vector=70, BR4
        not attached
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

A 14-word DEC paper-tape bootstrap was deposited but not executed. The words
were examined and verified immediately after deposit:

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

Unless SIMH persisted memory by some mechanism not evidenced here, those words
are now considered gone from the current machine state. They are evidence of
the exited session, not a claim about present RAM. The captured
`machines/pdp11/pdp11.conf` does not recreate them and remains an unchanged
copy of the earlier static configuration.

The verified listing above is sufficient to recreate the words
deterministically later. `machines/pdp11/late-summer-1970.simh` encodes a fresh
PDP-11/20 with 24 KB, CLK enabled, PTR enabled and unattached in a fresh SIMH
process, all later storage/tape/network devices disabled, and the 14 deposits.
It stops after displaying the configuration and memory; it contains no `go` or
boot command. The reconstruction script has deliberately not been run merely
to reproduce the former volatile evidence. It is 846 bytes, repository mode
0644,
SHA-256
`33402b10a72a613ecb36955379f4db8b5edf759589a9fdbfd0c7be9116d91a1d`.

## Stage 0 closure

Captured host/tool baseline: Ubuntu 26.04.1 LTS, Linux
`7.0.0-27-generic` x86-64, Git 2.53.0, Perl 5.40.1, and GCC 15.2.0.

The PDP-11 emulator/package discrepancy is resolved as a local-install fact:
Debian reports package `simh 3.8.1-6.3`, whose recorded MD5 for
`usr/bin/pdp11` is `79824a0bce88fa975b5b035995469c4a`; the installed binary's
MD5 is `2e85d81c40f594af331be4a439732af1`, and `dpkg -V simh` flags that file as
modified. The executable's embedded V4.0-0/`8a4b3752` identification and
SHA-256 recorded above therefore identify the actual emulator used; the Debian
package version does not.

Stage 0's static reproducibility record is now complete enough to recreate the
intended starting configurations without chat history. The first actual
project boots remain guarded verification operations: confirm the displayed
devices against this record before allowing either CPU to run, and do not
treat the reconstructed PDP-11 deposits as newly observed evidence.
