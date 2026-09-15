# Diskless PDP-11 cross-development and bring-up

## Historical hypothesis

This era models a diskless 24 KB PDP-11/20 receiving PDP-7-produced programs
by paper tape and executing them before Unix itself exists on the target. This
runnable state is not asserted as a named historical milestone or exact date.

## Evidence / provenance

PDP-7-to-PDP-11 paper-tape transport is historically attested. The exact Bell
Labs receiving loader and record format are unknown. The fourteen-word
bootstrap and 72-word DEC Absolute Loader are contemporary class A DEC
material used here as a class C substitute. The U1 tapes were produced by
class B native PDP-7 tools. Replay scripts and automation are class M. See
`evidence/b4/README.md` and `docs/SOURCES.md`.

## What exists

A clean PDP-11/20 KA11 configuration, loader materialization command, and two
replays using the committed native-PDP-7-produced U1 tapes: an interactive
interrupt/TRAP console demonstration and a noninteractive RAM-block diagnostic.
No Unix kernel, filesystem, RF11/RS11, or self-hosted toolchain exists.

## Run it

From the repository root, first materialize the archival DEC loader tape:

```sh
python3 tools/materialize_dec_loader.py
cd eras/pdp11-crossdev
pdp11 interrupt-trap.simh
```

Type `A` when prompted, wait for its echo, then type `B`. The optional RAM
diagnostic is available separately:

```sh
pdp11 ram-substrate.simh
```

## Try this

Watch the loader bring a program from the other machine's tape into memory,
then make it respond to your keyboard. Enter two ordinary characters, one at
a time, waiting for each echo. `AB` is the repeatable example, not a Unix
command. This machine has no shell yet.

## Expected result

The interrupt replay announces that the payload arrived through PTR, prompts
for two characters, echoes `AB`, and halts at PC `001070`. It then displays a
success word of `000001` at `003030`. The RAM replay loads through PTR, runs to
PC `001330`, and displays `000001` at `003042` plus its allocator results.
Those words are engineering checks; the public capability is receiving and
running software prepared on another machine. RAM testing is optional detail,
not a separate historical state or evidence that a filesystem exists.
Only the fourteen-word bootstrap is entered directly. Both substantial test
programs are native `as11` output and enter through PTR; the replay files do
not deposit their words.

## Acceptance / regression

`python3 tools/run_b4_transport.py` independently verifies tape checksums,
word-for-word loaded memory, real bootstrap/loader execution, and both U1
results. `python3 -m unittest tests.test_eras` checks that the human replays
contain no target-payload deposits and consume the committed tapes unchanged.

## Known uncertainties

DEC loading is not claimed as Bell Labs' actual loader. U1 contains project
machine diagnostics, not a recovered historical program. The replay automates
front-panel entry and media handling while preserving the paper-tape loading
steps. This is cross-developed target execution, not PDP-11 self-hosting.
