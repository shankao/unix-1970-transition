# PDP-7 to PDP-11 cross-development

## Historical hypothesis

This era models the historically attested cross-development situation in
which PDP-11 programs were prepared on PDP-7 Unix and punched for transport.
It is a current capability slice, not a claim that the reconstructed tools or
filesystem reproduce one exact Bell Labs date.

## Evidence / provenance

PDP-7 Unix and its restored B environment derive from surviving material.
`as11` and the DEC absolute-tape formatter are class B reconstructions. The
authentic PDP-7 PTP path is used; DEC absolute-binary formatting is a class C
period substitute because the Bell Labs tape format and receiver are unknown.
Host runners are class M. See `docs/PDP7-AS11.md` and `evidence/b4/`.

## What exists

The self-contained disk retains the native B-hosted `as11`, accepted U1 traces,
the native absolute-tape formatter sources, and the concise `shankao/readme`.
The assembler is a validated bootstrap nucleus, not a complete PDP-11
assembler or recovered Bell Labs program. The selected `pdp7.fs` SHA-256 is
`0a7a3589b13a4b4732b20cfa5c1afe5ed14474e2a62670add1e29016b8525dba`.

## Run it

From this directory:

```sh
pdp7 pdp7.simh
```

## Try this

Log in as `shankao` / `shankao`, then run `cat readme` and `stat abspun.b`.

## Expected result

The first summarizes the working cross-development state; the second reports
the retained PDP-7-side tape formatter source. Punching itself uses the
authentic `dd/system/pptout` device and is deliberately exercised by the B4
acceptance runner rather than by an unsafe abbreviated manual recipe.

## Acceptance / regression

`python3 tools/run_b4_transport.py` proves native `as11` output, PDP-7 PTP
production, and the receiving PDP-11 path. The documented launch and native
file checks were exercised directly during era creation; `python3 -m unittest
tests.test_eras` guards the era/snapshot structure.

## Known uncertainties

The exact 1970 Bell Labs assembler, tape writer, tape records, and receiving
loader are lost or unidentified. Runnability does not raise their evidence
class. The image also contains accumulated project diagnostics beyond what a
historical operator necessarily saw.
