# UNIX 1970: Across the Floor

Run a few reconstructed 1970 machine states and watch capabilities appear.
Start with a working PDP-7 Unix, use it to assemble code for a new PDP-11/20,
then take a virtual paper tape to that machine and see it answer at the
console. How much could they make happen with almost nothing?

The journey currently reaches standalone PDP-11 programs. Unix runs on the
PDP-7; the PDP-11 has 24 KB of core and no Unix or disk yet. With no network or
shared disk between these machines, and the development tools on the PDP-7,
paper tape gives the new machine a way to receive its software.

## Try the journey

Use SIMH `pdp7` and `pdp11`. Commands below start at the repository root;
[the running guide](docs/RUNNING.md) covers setup, prompts, and leaving each
machine.

| Enter this state | What has appeared? | Launch and try |
| --- | --- | --- |
| [A working PDP-7 Unix](eras/pdp7-unix/ERA.md) | Unix already provides a place to log in, keep files, and work. | `cd eras/pdp7-unix`, then `pdp7 pdp7.simh`. Log in as `shankao` / `shankao` and try `ls`. |
| [Write for the PDP-11 on the PDP-7](eras/pdp7-crossdev/ERA.md) | A B-hosted PDP-11 assembler and tape formatter are runnable. | `cd eras/pdp7-crossdev`, then `pdp7 pdp7.simh`. Follow the guide to edit `demo.s`, run `as11`, and punch that exact result. |
| [Bring the tape to the PDP-11](eras/pdp11-crossdev/ERA.md) | The new machine receives a program through its paper-tape reader and responds to your keyboard. | Prepare the loader and launch the replay below. Type `A`, wait for its echo, then type `B`; the program echoes both and halts. |

For the receiving-machine experience, from the repository root:

```sh
python3 tools/materialize_dec_loader.py
cd eras/pdp11-crossdev
pdp11 interrupt-trap.simh
```

The replay uses a committed tape actually punched by the emulated PDP-7. It
automates entering the small bootstrap and changing tapes; the PDP-11 itself
reads and executes the loader, then reads the program. The filename reflects
the diagnostic underneath, but what you experience is software arriving from
another machine and making the console respond.

**Continue with [the guided journey](docs/RUNNING.md)** for native assembly,
the visitor-created tape steps, the richer accepted console tape, and optional
machine diagnostics.

## What is reconstructed?

These are our current best runnable models of plausible historical states.
They divide a continuous transition into a few runnable states without
inventing exact dates. Each state gives a person something new to do; research
can change them later.

The general PDP-7-to-PDP-11 paper-tape transfer is historically attested. Bell
Labs' exact receiving loader and tape format remain unknown. The 14-word DEC
bootstrap and 72-word Absolute Loader provide a conservative contemporary
**class-C substitute**. Successful execution does not establish that Bell Labs
used them. The assembler and demonstration programs are reconstructions, not
recovered 1970 source. Later surviving Unix material is descendant evidence,
not automatically a specification for 1970.

[Method and provenance](docs/METHOD.md) distinguishes authentic material (A),
conservative reconstruction (B), contemporary substitutes (C), unknowns (D),
and modern instrumentation (M). [Sources](docs/SOURCES.md) and each era's
`ERA.md` explain the evidence and remaining uncertainty.

## Where this leads

The intended continuation is core-only PDP-11 Unix and then the first
disk-backed environment associated with the 1970 RF11/RS11 transition. Neither
is runnable today. The surviving/restored PDP-7 system supplies the principal
migration workload. Bootstrap/B-tool work and Unix migration proceed along
parallel tracks; the full edit-B → compiler → assembler → tape → PDP-11
“Across the Floor” sequence is still ahead.

For contributors, [STATUS](docs/STATUS.md) records B4 and U1 complete and U2
unstarted; [PLAN](docs/PLAN.md) holds the R/B/U engineering milestones and
acceptance gates. They support the public journey without determining its
state boundaries. [UNIX-MIGRATION](docs/UNIX-MIGRATION.md) and
[STATE](docs/STATE.md) link the contracts and machine records.

Git preserves how the reconstruction evolved. [`snapshots/`](snapshots/),
tests, and `evidence/` retain selected project states and technical results.
[`eras/`](eras/) presents the living historical-system reconstructions.

## Licensing

Original project work normally uses [GPL-3.0-only](LICENSE). Imported,
restored, historical, and generated material retains its own applicable
notices and provenance. See [the mixed-provenance licensing policy](LICENSES/README.md).
