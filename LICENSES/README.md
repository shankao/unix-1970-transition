# Licensing and Imported Material

No repository-wide license has been selected yet.

Reason: this project is expected to combine newly written reconstruction code with references to historical source/restoration projects that have different provenance and licensing.

Before importing any external source, record:

- upstream project/archive;
- exact commit/version;
- original file path;
- copyright notice;
- license;
- whether redistribution is permitted;
- local modifications.

## Imported PDP-7 host

`machines/pdp7/` was copied from the local pre-transition/reference machine
`../PDP-7/` on 2026-08-31. Nested Git metadata was intentionally omitted. The
copy contains two DoctorWkt `pdp7-unix` working trees:

- `pdp7-unix`, based on upstream commit
  `e3ebcef20488b33eba8a7479cbd98b64e8af438b` with retained local changes;
- `pdp7-unix-copy`, based on upstream commit
  `555eb30fc76b8fa29095d32eca9a43e9b1638288` with retained local changes.

Upstream: <https://github.com/DoctorWkt/pdp7-unix>

Each imported tree retains its upstream `LICENSE` (GPLv3) and `README.md`.
The upstream README separately states that code derived from scans is owned by
Micro Focus and that material not derived from scans is GPLv3. Consequently,
the import is not classified under one undifferentiated license: provenance of
individual files remains governed by the upstream distinction. The local
filesystem images, build products, account, and exploratory files are retained
as machine state rather than represented as authentic Bell Labs source.

The exact imported paths, sizes, modes, and SHA-256 hashes are recorded in
`evidence/pdp7-import-manifest.tsv`.
