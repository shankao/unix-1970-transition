# Stage 4A evidence

This directory is class **M** capture/evidence for the class-B PDP-7 rewind
helper and B probe.

- `session.transcript.txt`: successful native `shankao` compile, assembly,
  execution, and result display.
- `result.txt`: canonical 472-character PDP-7-generated output.
- `image-state.txt`: pre/post authoritative image hashes and Git status.
- `initial-failure.txt`: retained transfer/link failure and diagnosis.
- `checkpoint.txt`: final image hash, integrity result, and native artifact
  inventory used to close the machine checkpoint.

| File | SHA-256 |
| --- | --- |
| `session.transcript.txt` | `5d8af1c2c51d045fccfa9b69364cf9d40a5730dad7cf2e670788b8cd8b525e19` |
| `result.txt` | `eea79ca9f64b98e07cce526b75ed124eeb38d22b4f1d5b7364c2959d95017710` |
| `image-state.txt` | `42c6db300e142ad86c1013c5deef3300437ecc67d80c0acd7291bd8397110d5c` |
| `initial-failure.txt` | `47f0a7beb90046111b0eeeebf36a001f76cd5ad016960f98f63361bb21fee840` |
| `checkpoint.txt` | `a24a3ed5b3072a64073047f21ddbb8a542a4c4315ae471a9caafe8379bc00972` |

The run used authoritative `machines/pdp7`, not a disposable copy. The image
changed intentionally, was not restored, and is preserved by the Stage 4A
follow-up machine checkpoint.
