# Licensing and Provenance Policy

This is a multi-license, mixed-provenance repository. The root
[`LICENSE`](../LICENSE) applies as `GPL-3.0-only` to project-original
`unix-1970-transition` material unless a file or directory says otherwise. It
does not relicense imported, restored, historical, or generated material over
which this project does not hold the necessary rights.

License and provenance are separate dimensions. The A1/A2/B/C/D ancestry in
[`docs/UNIX-MIGRATION.md`](../docs/UNIX-MIGRATION.md) describes historical
source relationships; it does not determine copyright or redistribution
terms. Future source should record both when derivation matters.

## Project-original material

Original project documentation, modern tools and tests, PDP-11 reconstruction
source, and independently written assembler extensions are normally
`GPL-3.0-only`. This classification applies only after checking that the file
is genuinely project-original rather than a close adaptation or import.

New project-original source and documentation should normally carry:

```text
SPDX-License-Identifier: GPL-3.0-only
```

Do not mass-apply this identifier. Historical source, imports, close
derivatives, generated files, and preserved eras require their own review. A
new independent reconstruction informed by documented PDP-7 responsibilities
may also identify that provenance in a comment and point to
`docs/UNIX-MIGRATION.md`; that statement does not assert ownership of, or
relicense, the historical material.

## DoctorWkt PDP-7 restoration import

`machines/pdp7/pdp7-unix/` came from the DoctorWkt `pdp7-unix` restoration,
based on upstream commit `e3ebcef20488b33eba8a7479cbd98b64e8af438b`
with retained local changes. Upstream:
<https://github.com/DoctorWkt/pdp7-unix>.

The imported tree retains its upstream [`LICENSE`](../machines/pdp7/pdp7-unix/LICENSE)
and README. Upstream describes restoration material not derived from scans as
GPLv3, and individual modern tools/source carry notices for Warren Toomey or
Robert Swierczek. Those notices must remain. A close adaptation—such as a
future `b11` directly based on Robert Swierczek's restored compiler—must retain
the applicable GPL and upstream attribution rather than be represented as an
independent project implementation.

The original import also contained `pdp7-unix-copy`, based on upstream commit
`555eb30fc76b8fa29095d32eca9a43e9b1638288`. A later audit found it to be an
unused older subset; Git and `evidence/pdp7-import-manifest.tsv` preserve its
provenance and exact imported bytes.

## Historical PDP-7 material

The DoctorWkt README and `scans/README.md` explicitly distinguish material
derived from historical scans, including material attributed there to Micro
Focus, from the GPL restoration work. The familiar permissions associated
with later Ancient Unix or Caldera releases must not be assumed to cover this
PDP-7 corpus automatically.

Historical listings, transcriptions, and closely derived restored source
retain the licensing status supplied by their upstream/historical source and
are not relicensed by `unix-1970-transition`. Where the exact status of an
individual historical file is unclear, record it as unclear and preserve its
notices and provenance rather than applying the root license by directory.

## Other third-party material

Other imported code, emulator material, documentation, or data retains its
applicable upstream license and copyright notices. Before copying or closely
deriving from it, record the upstream project/archive, version or commit,
original path, notices, license, redistribution basis, and local changes.
Directory placement alone never establishes a license.

## Current path audit

This is a policy-level audit, not a claim that every historical file has
completed line-by-line rights analysis:

| Path/material | Current classification |
|---|---|
| `README.md`, `AGENTS.md`, `docs/` | Project-original documentation, except any clearly identified quotation or imported text; default `GPL-3.0-only`. |
| `tools/`, `tests/` | Project-original class-M orchestration and tests; default `GPL-3.0-only`, subject to any file-specific notice. |
| `src/pdp11/` | Project-original conservative reconstruction informed by recorded evidence; default `GPL-3.0-only`, with historical provenance documented separately. |
| `src/pdp7/as11/` | Project-original reconstruction and extensions, not surviving Bell Labs source; default `GPL-3.0-only`. Any future close upstream adaptation requires reclassification. |
| `machines/pdp7/pdp7-unix/` | DoctorWkt/restoration import with mixed GPL restoration and historical scan-derived material; upstream notices control. |
| `machines/pdp7` filesystem image and native products | Generated/evolving machine state incorporating mixed-provenance material; no automatic independent GPL classification. |
| `machines/pdp11/` configs | Project-original machine configuration where not supplied by SIMH or another upstream; default `GPL-3.0-only`. |
| `artifacts/`, `evidence/` | Mixed: project records plus generated output and copies of evidence; classify by producing or incorporated material. |
| `eras/` | Preserved generated machine/configuration states, often incorporating historical/restoration material; no blanket relicense. |

No additional third-party source license was found in `src/`, `tools/`, or
`tests/` during this policy audit. That absence is not permission to ignore a
future derivation discovered at file or commit level.

## Generated and preserved material

Binaries, filesystem images, boot images, generated assembly/output, and
preserved eras do not acquire an independent GPL license merely because this
repository generated or stores them. Their redistribution status can depend
on incorporated source and data. Preserve the producing-source provenance and
do not add SPDX headers to generated or experiential artifacts without a
specific review.

Current examples include the PDP-7 filesystem images and bootstrap-bearing
eras, which incorporate mixed historical/restoration material, and PDP-11
deposit scripts generated from project reconstruction source. This policy
classifies their provenance; it does not make a new claim about ownership.
