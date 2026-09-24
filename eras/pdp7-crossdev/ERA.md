# PDP-7 to PDP-11 cross-development

## Historical hypothesis

This era models the historically attested cross-development situation in
which PDP-11 programs were prepared on PDP-7 Unix and punched for transport.
It is a current runnable state, not a claim that the reconstructed tools or
filesystem reproduce one exact Bell Labs date.

## Evidence / provenance

PDP-7 Unix and its restored B environment derive from surviving material.
`as11` and the DEC absolute-tape formatter are class B reconstructions. The
authentic PDP-7 PTP path is used; DEC absolute-binary formatting is a class C
period substitute because the Bell Labs tape format and receiver are unknown.
The three-word `demo.s` and host runners are class M teaching/operator aids,
not historical Bell Labs programs. See `docs/PDP7-AS11.md` and `evidence/b4/`.

## What exists

The self-contained disk retains the native B-hosted assembler as `as11`, the
native formatter as `abspun`, an editable `demo.s`, accepted U1 traces, native
formatter sources, and the concise `shankao/readme`.
The assembler is a validated bootstrap nucleus, not a complete PDP-11
assembler or recovered Bell Labs program. The selected `pdp7.fs` SHA-256 is
`d2e7cd48703c80096ce64ea04ab55acfb6c219458b17e12261129ff2a212954b`.
The first Unix workload added `sub`, `beq`, and `dec`; the installed command
uses 16-word B input/output buffers so real source fits without overlapping
the assembler's symbol and stack area. Its global and local tables use space
released below the smaller buffers. Ordinary Unix builds run on disposable
copies of this image and do not leave source, output, or `a.out` scratch files
here.
The normal way to create a substantial PDP-11 program in this state is to keep
readable symbolic source and assemble it with `as11`; direct word entry is
reserved for amounts a programmer could plausibly enter by hand.

## Run it

From this directory:

```sh
pdp7 pdp7.simh
```

## Try this

Log in as `shankao` / `shankao`. Follow the
[guided editor exercise](../../docs/RUNNING.md#2-write-for-a-machine-that-has-no-unix-yet--pdp-7)
to edit and assemble `demo.s` with `as11`. Quit PDP-7, then from the repository
root run:

```sh
python3 tools/punch_era.py demo.o
pdp11 artifacts/visitor/demo.simh
```

## Expected result

The PDP-7-created trace is punched through authentic `dd/system/pptout`, then
read by the PDP-11 through PTR, bootstrap, and Absolute Loader. The sample
halts with R0 equal to the immediate value you assembled. Python is class-M
operator automation and validation; it does not encode the payload.

## Acceptance / regression

`python3 tools/run_b4_transport.py` proves native `as11` output, PDP-7 PTP
production, and the receiving PDP-11 path on the development host. The public
`punch_era.py` path independently proves that visitor-created era output feeds
that same punch/reader mechanism. `python3 -m unittest discover -s tests`
guards both paths and the era/snapshot structure.

## Known uncertainties

The exact 1970 Bell Labs assembler, tape writer, tape records, and receiving
loader are lost or unidentified. Runnability does not raise their evidence
class. The image also contains accumulated project diagnostics beyond what a
historical operator necessarily saw.
