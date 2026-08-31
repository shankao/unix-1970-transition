# Tools

## 3dump

An application which dumps PDP-7 binary files

## a7out

User-mode simulator for PDP-7 Unix applications

## adduserdir7

Copies an existing original-layout (`dd`) SimH filesystem image and adds a
user directory without rebuilding the image from `proto`. It preserves changes
made from inside Unix, refuses to replace either image, follows the kernel free
block allocator (including chained-list cache refills), and publishes the new
image atomically.

The UID is octal. For example:

```
tools/adduserdir7 build/image.fs build/image-new.fs alice 20
```

The new directory contains the historical `dd`, self-referential `..`, and
`system` links. This tool is not for the alternative filesystem, which has no
`dd` directory and uses modern `.` and `..` entries.

Run its integration tests against a built image with:

```
tools/test-adduserdir7 build/image.fs
```

## as7

An assembler for PDP-7 assembler files

## b.c

A prototypical compiler for the B language

## fsck7

Check and dump the details of a PDP-7 filesystem image for SimH

## mkfs7

Makes a PDP-7 filesystem image for SimH

## sdump

A tool to dump the contents of the ../build/image.fs filesystem

## xref7

A quick and nasty tool to cross-reference the kernel code
