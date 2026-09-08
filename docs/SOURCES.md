# Source Register

This is a working source register, not a bibliography dump. Each entry should state what it actually supports.

## Primary / near-primary historical accounts

### Dennis M. Ritchie — *The Evolution of the Unix Time-sharing System*

Canonical page:
https://www.nokia.com/bell-labs/about/dennis-m-ritchie/hist.html

Supports, among other points:

- a PDP-7 B cross-compiler for the PDP-11 existed and was written in B;
- B moved to the PDP-11 very early;
- a version of multi-precision `dc` ran on the PDP-11 before the disk arrived;
- the early diskless/RAM-disk PDP-11 period preceded the usable First Edition
  system;
- the first disk arrived around December 1970, which supports this
  repository's endpoint without implying later First Edition work was already
  complete;
- modern `exec`, modern `wait`, and full pathnames are described with the
  first completed PDP-11 system after disk arrival; the account does not fix
  their exact introduction within the earlier pre-disk interval.

### Dennis M. Ritchie — *The Development of the C Language*

Canonical PDF:
https://www.nokia.com/bell-labs/about/dennis-m-ritchie/chist.pdf

Supports:

- the PDP-11 was received before its disk;
- making B run on the PDP-11 required threaded-code operator fragments;
- Ritchie coded a simple PDP-11 assembler in B;
- `dc` became the first interesting program tested before an operating system;
- the machine had 24 KB and an earliest test system later divided memory among OS, tiny user area, and RAM disk.

### Ken Thompson oral history

TUHS archive:
https://www.tuhs.org/Archive/Documentation/OralHistory/transcripts/thompson.htm

Supports the practical cross-development workflow, including the B-written PDP-11 assembler running on the PDP-7 and paper tape being moved from the PDP-7 to the PDP-11.

## Surviving/reconstructed PDP-7 UNIX

### DoctorWkt/pdp7-unix

https://github.com/DoctorWkt/pdp7-unix

Important provenance note from upstream:

- the project was built from scans of original assembly code;
- upstream separates scanned/original material from later restoration code;
- upstream states that scanned UNIX source has different ownership from newly written restoration code.

This repository must preserve that distinction if any material is imported.

For UNIX migration work, the restored tree is the principal local source base
but is not one uniform provenance class. The layered A1/A2/B/C/D source model
and provisional v1 audit in [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md)
distinguish the Norman Wilson/companion-binder and Ritchie Book II listing
lineages, restored working derivatives, local repair/interpretation, and other
material. The audit records strong source-level ancestry; it does not claim a
complete line-by-line provenance map or that every restored file is untouched
contemporary source.

The checked-in `scans/` and restored `src/` pairs support the provisional v1
source-level audit of `s1.s`–`s9.s`, `cat.s`, `ls.s`, `rm.s`, `sh.s`, and
`stat.s`. [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md) records responsibility-level
selection and deferral; neither file presence nor runnable status proves that
the working file is an unmodified contemporary original.

For Stage 4A, the checked-in local copies
`machines/pdp7/pdp7-unix/src/cmd/bl.s`, `src/sys/s2.s`, and `src/cmd/as.s`
are direct implementation evidence for the recovered B input buffer and EOF
behavior, kernel `seek`, and authentic PDP-7 assembler syscall syntax. They do
not establish the lost PDP-11 `as11` language or source.

## B archaeology/reconstruction

### Ken Thompson — *User's Reference to B* (7 January 1972)

Bell Labs internal memorandum, especially section 12, “Implementation and
Debugging.” Authentic documentation of the later PDP-11 B direct-threaded
implementation: R3/R4/R5 roles, frame layout, word/byte address scaling,
`jmp *(r3)+` dispatch, and printed `va`, `x`, `c`, `b12`, and `b1` fragments.
It postdates the project's late-1970 target and is not surviving source for the
original diskless runtime; it constrains the class-B Stage 3A reconstruction.

### Angelo Papenhoff (`aap/b`)

https://github.com/aap/b

Supports/references:

- modern reconstruction of B and its original threaded-code model;
- B compiler structure using a B first pass and target/assembler-dependent second pass;
- reconstructed UNIX V1 PDP-11 B environment based partly on discovered binaries;
- useful later PDP-11 runtime material for archaeological comparison.

This is not evidence that its exact source layout or runtime equals the lost diskless-1970 implementation.
The binary-derived older/V1 `obrt1` reconstruction is corroborating B/C
reference evidence for the R3/R4/R5 model and the four-instruction `n11`
frame unwind recorded in `PDP11-B-RUNTIME.md`. Do not use the separately described
`unix1_bdir/int` design as historical evidence; its author labels that
interpreted-code design speculative. No `aap/b` code was imported in Stage 3.

## Contemporary DEC documentation

### DEC — *PDP-11 Handbook*, Second Edition (1970)

Primary authority for the base KA11/PDP-11/20 instruction formats, eight
addressing modes, PC-special modes, branch displacements, little-endian word
layout, console device addresses/vectors, and contemporary software-arithmetic
examples. It constrains the class-M Stage 2 oracle and the Stage 3 instruction
boundary. Use the exact 1970 second edition from the DEC PDP-11 handbook
archive; the printed `CMPB @#177560,#301` example is retained as a gold vector.

### DEC — *PDP-11/20 Price List*, 1 November 1970

Primary commercial documentation establishing KE11-A as separately priced
extended-arithmetic hardware for the PDP-11/20. It supports keeping KE11
disabled and does not justify accepting the later EIS `MUL`, `DIV`, `ASH`, or
`ASHC` CPU instructions.

### PDP-11 Paper Tape Software Programming Handbook

Bitsavers copy:
https://www.bitsavers.org/www.computer.museum.uq.edu.au/pdf/DEC-11-XPTSA-A-D%20PDP-11%20Paper%20Tape%20Software%20Programming%20Handbook.pdf

Use for contemporary DEC paper-tape software, loader formats, device conventions, and PDP-11 programming details.

If DEC Absolute Binary or another DEC loader is used in the experiment, its role must remain class C unless evidence establishes that Bell Labs used the same format.

### PDP-11 Conventions / handbooks

Bitsavers index:
https://www.bitsavers.org/pdf/dec/pdp11/handbooks/

Use exact dated editions wherever possible.

## Source-management rule

When a source becomes important to an implementation decision, add:

- exact edition/date;
- exact URL or archive identifier;
- page/section or quoted claim location;
- local archived hash if a copy is retained;
- the decision(s) it constrains.
