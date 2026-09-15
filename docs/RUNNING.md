<!-- SPDX-License-Identifier: GPL-3.0-only -->
# From a working Unix to a program across the floor

Follow three runnable states: explore Unix on the PDP-7, write instructions
for the PDP-11 there, then bring a tape to the new machine and run it. Each
state lets you do something new. We chose these divisions to show historical
change, not because of dates or project milestones.

## Before you start

You need SIMH `pdp7` and `pdp11` on your path and Python 3 for the small loader
media preparation command. The PDP-7 emulator must support the restored
RB/GRAPHICS-2 devices used by this repository; the imported build and machine
details are in [STATE](STATE.md). From an era directory, the repository's
existing built emulator can also be addressed as
`../../machines/pdp7/pdp7-unix/build/pdp7` if your installed `pdp7` differs.

Start each numbered section from the repository root in your host terminal.
Run only one PDP-7 at a time: both configurations use terminal port 12345.
Log in at the emulator's `login:` prompt. The example account and password are
both `shankao`; this account is a project convenience, not a historical identity.

PDP-7 shell commands below follow its `@ ` prompt; editor commands follow
`edit`. Type one line at a time, waiting for its echo; avoid pasting a whole
block at speed. `#` erases a character and `@` kills an input line. See the
[native tool notes](PDP7-TOOLS.md) for differences from later Unix.

To leave a machine, press Ctrl-E to reach SIMH's `sim>` prompt, then type
`quit`. PDP-7 sessions write their local disk image, so your files can survive
a restart. Snapshots preserve earlier project states separately.

## 1. A Unix you can work in — PDP-7

**What is here:** Unix already runs, with a shell, files, an editor, and
restored commands. This is the working environment from which the transition
begins.

```sh
cd eras/pdp7-unix
pdp7 pdp7.simh
```

Log in as `shankao` / `shankao`, then type:

```text
ls
```

You should see files such as `hello.s` and `ps.s`, followed by the shell prompt.
The account also contains project exploration files; the
[era manifest](../eras/pdp7-unix/ERA.md) explains the mixture of surviving,
restored, and reconstructed material. Leave SIMH before entering the next state.

## 2. Write for a machine that has no Unix yet — PDP-7

**What is new:** a reconstructed B-hosted PDP-11 assembler is available.
You can turn readable instructions for the new machine into actual target
words while still working inside PDP-7 Unix. The already-proven native tape
formatter is installed too, so the exact words you assemble can leave through
the PDP-7 paper-tape punch.

```sh
cd eras/pdp7-crossdev
pdp7 pdp7.simh
```

Log in as `shankao` / `shankao`. The reconstructed tools have stable names:
`as11` is the assembler and `abspun` is the DEC absolute-tape formatter.
Native builds still produce `a.out`, but no public tool is hidden under that
ambiguous name.

The image includes a small source file whose result is easy to recognize on
the PDP-11. Load it with the native editor and, if you like, change octal
`101` to `102`. Enter each line separately:

```text
ed
r demo.s
/101/
s/101/102/
w
q
```

At the shell prompt, assemble the saved source and inspect its exact native
word trace:

```text
as11 demo.s demo.o
cat demo.o
```

If you made the suggested edit, expected output is:

```text
i 001000 012700
x 001002 000102
i 001004 000000
```

The PDP-7 has encoded a PDP-11 instruction to put `102` in R0, followed by
HALT. (`101` appears if you skipped the edit.) The `i` records are instructions
and `x` is the immediate word. Nothing on the host has encoded them.

### From assembler output to paper tape

The PDP-11 has neither Unix nor a disk holding these tools. There is no network
or shared disk joining the two machines in this reconstruction. The PDP-7
punch puts the program on a medium the PDP-11 can read.

Quit the PDP-7, return to the repository root, and punch the exact `demo.o`
you just made:

```sh
python3 tools/punch_era.py demo.o
```

This class-M wrapper reads `demo.o` from the era disk, temporarily links it and
the installed `abspun` into the authentic `system` directory, and captures
output from `dd/system/pptout`. That narrow super-user step is required by the
surviving special-file layout; it does not grant `shankao` new privileges.
The wrapper verifies the resulting DEC records against the native trace but
does not create, replace, or repair target bytes. It writes the tape and a
short operator replay under `artifacts/visitor/`.

## 3. Bring the tape to the new machine — PDP-11/20

**What is new:** software arrives from the PDP-7 and gives the diskless PDP-11
something to execute. No Unix prompt will appear here yet. The console's
response comes from the loaded program itself.

First carry the tape you just punched to the PDP-11:

```sh
pdp11 artifacts/visitor/demo.simh
```

The punch command has materialized the archival loader tape alongside your
tape; it has not generated your program. The replay performs this path:

```text
14-word bootstrap entered through the emulated front panel
    -> PTR reads the 72-word DEC Absolute Loader
    -> that loader reads the PDP-7-produced program tape
    -> the program appears in PDP-11 memory and starts
```

The bootstrap and loader each halt as part of tape changing; the script
continues automatically. Your three-word program then halts at PC `001006`
and SIMH shows `R0: 000102` (`000101` without the edit). Your source change on
the PDP-7 has crossed the machine boundary as paper-tape bytes and changed the
PDP-11 result.

For a richer existing program, use the accepted console tape:

```sh
python3 tools/materialize_dec_loader.py
cd eras/pdp11-crossdev
pdp11 interrupt-trap.simh
```

At `U1 INTERRUPT/TRAP TAPE LOADED - TYPE AB`, type `A`, wait for its echo,
then type `B`. The machine echoes both and halts at PC `001070`.

That program also works with two ordinary characters such as `ki`, entered one
at a time. `AB` is the reproducible example used by the acceptance tests.
The [era manifest](../eras/pdp11-crossdev/ERA.md) records what else the program
checks internally.

The general paper-tape transfer is historically attested, but Bell Labs' exact
loader and tape format are unknown. The DEC bootstrap, Absolute Loader, and
absolute-binary format are a contemporary **class-C reconstruction choice**.
Running them successfully does not make that choice historical fact.

### Optional: look beneath the experience

From the same era directory, `pdp11 ram-substrate.simh` loads a second tape
and runs the RAM-block diagnostic. It halts at PC `001330`, showing exhaustion
`177777`, reused block `000002`, and success `000001`. This is engineering
evidence for storage primitives; it is not a filesystem or another public
historical state. [The B4 evidence](../evidence/b4/) and
[technical status](STATUS.md) cover the full checks.

## What comes later

The current journey ends here. A RAM-backed PDP-11 Unix with files and a shell,
and eventually persistent RF11 storage, are future experiences. A completed
engineering milestone earns a new public state only when it gives a visitor a
meaningful new capability. [METHOD](METHOD.md) records that rule and the
separation between living historical models, project snapshots, and Git history.
