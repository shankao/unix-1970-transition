# Reconstruction snapshots

These directories preserve what this modern reconstruction project had
established at named project checkpoints. They are reproducibility records,
not claims that Bell Labs passed through matching historical eras.

The Stage-labelled directories were moved here intact from `eras/` when the
repository distinguished project history from reconstructed historical-system
history. Their original manifests, media, configurations, hashes, and project
milestone language are deliberately retained. Git records their former paths.
`pdp11-crossdev/` likewise preserves the earlier polling-only project
checkpoint that first established cross-developed PDP-11 execution; the living
historical era now incorporates B4 paper-tape transport.

Each PDP-7 snapshot remains directly bootable from its directory with:

```sh
pdp7 pdp7.simh
```

Current historical-system reconstructions live under [`../eras/`](../eras/).

## Classification audit

| Former `eras/` directory | Classification | How it relates to the historical system |
| --- | --- | --- |
| `stage-0` | project snapshot | Earliest imported runnable PDP-7 baseline; selected as the medium for the current late-PDP-7 era, with its project additions disclosed. |
| `stage-1` | project snapshot | B-characterization checkpoint; evidence about the host, not a distinct historical-system boundary. |
| `stage-4a` | project snapshot | Modern two-pass-I/O implementation checkpoint; no evidence for a matching Bell Labs era. |
| `stage-4b` | project snapshot | Modern parser/symbol implementation checkpoint; no evidence for a matching Bell Labs era. |
| `stage-4c` | project snapshot | Modern encoder/capacity checkpoint; contributes to the cross-development hypothesis but is not independently an era. |
| `pdp11-crossdev` | project snapshot | First polling-only exact-word execution checkpoint; useful evidence retained here, while the living era now reflects B4 paper-tape loading. |

All six were runnable at the time of audit. Their manifests primarily described
what this project had completed, and later B4 evidence had already made the
PDP-11 directory's deposit-only transport an obsolete historical-era model.
