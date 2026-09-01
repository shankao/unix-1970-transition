# Evidence Area

This directory stores claim-level inventories, generated representations, and
captured execution evidence. Evidence is not automatically class A: generated
manifests, emulator scripts, transcripts, and hashes are normally class M and
their README states the boundary.

Current major groups include:

```text
pdp7-import-manifest.tsv       immutable Stage 0 import inventory
pdp7-b-inventory.tsv           Stage 1 B component inventory
pdp7-b-stage1-results.tsv      Stage 1 probe/result index
pdp7-b-static/                 static compiler/runtime comparisons
pdp7-b-stage1/                 captured compiler/runtime probe evidence
stage3a/                       threaded-nucleus deposits and transcripts
stage3b/                       control/call deposits and transcripts
```

Do not commit third-party scans/binaries merely because they are publicly downloadable. Check redistribution rights first; otherwise store URL, metadata, hash, and local retrieval instructions.
