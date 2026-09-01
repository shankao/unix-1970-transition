# PDP-11 threaded-B runtime reconstruction

## Scope and provenance

Stage 3 is split because the direct-threaded nucleus has unusually strong
technical evidence while the late-1970 control, call, return, and frame
machinery is less certain. **Stage 3A** reconstructs and executes only the
strongly evidenced nucleus. **Stage 3B** remains open for the rest of the
minimal runtime.

The historical architecture is class **A** evidence: Dennis Ritchie records
that B reached the 1970 PDP-11 through threaded operator fragments, and Ken
Thompson's authentic 7 January 1972 *User's Reference to B* prints the PDP-11
register conventions, frame layout, dispatch, and several operator bodies.
The manual postdates the late-1970 diskless target, so it is strong evidence of
the lineage, not proof that its text is the lost 1970 source.

The source in `src/pdp11/threaded-b/core.s` is therefore class **B**
conservative reconstruction. The binary-derived older/V1 `obrt1` work in
Angelo Papenhoff's `aap/b` corroborates R3/R4/R5 and several fragments, but is
B/C reference evidence, not original 1970 material. Its separately described
`unix1_bdir/int` interpreted design is speculative and is not evidence or an
input here. No third-party code was imported.

The Stage 2 oracle, fixed-address builder, word manifest, explicit SIMH
deposits, transcript capture, and synthetic test data/frame are class **M**.
They are diagnostic machinery and are excluded from the eventual PDP-7 tool ->
paper tape -> bare PDP-11 historical path.

## Execution model

- R3 is the interpreter program counter. The threaded stream consists of
  operator byte addresses followed by operands where required.
- R4 is the display pointer/current frame base.
- R5 is the B expression stack pointer. The hardware SP is not the B stack.
- Ordinary fragments end with `jmp @(r3)+`, directly fetching and dispatching
  the next operator address.
- A frame has previous display pointer at word 0, saved interpreter PC at word
  1, and automatics from word 2 onward.
- B lvalues/pointers are word addresses, while the PDP-11 addresses bytes.
  `va` divides a byte address by two with `ASR`; `b1` multiplies the B address
  by two with `ASL` before storing.

## Stage 3A fragments

The readable assembly preserves Thompson's documented instruction sequences
for all five ordinary operators:

- `c`: consume one stream word and push it on the R5 stack.
- `x`: consume an external byte address, load its word, and push the value.
- `va`: add the stream frame offset to R4, convert the byte address to a B word
  address with `ASR`, and push it.
- `b12`: pop the top expression value and add it into the preceding value.
- `b1`: pop value and B word-address lvalue, scale the address with `ASL`,
  store, then push the assigned value.

`start`, `emit`, and `stop` are project scaffolding, not documented original
B fragments. `start` initializes R3/R4/R5 and enters direct dispatch. `emit`
pops one value, polls KL11 TPS `177564`, writes its low byte to TPB `177566`,
then waits for TPS ready again before dispatch. `stop` executes `HALT`.

The second wait is the only behavior added after an observed failure. The
first A run reached HALT but SIMH had not serviced the queued transmitter
character. Its transcript is preserved as
`evidence/stage3a/test-a-initial-failure.transcript.txt`. Waiting for ready
after the write makes completion observable before an immediately following
HALT; it changes only the project `emit` service, not Thompson's operators.

## Fixed test layout

All locations are octal PDP-11 byte addresses and are M-class test placement:

| Area | Address |
| --- | ---: |
| startup | `001000` |
| `c`, `x`, `va`, `b12`, `b1` | `001100`–`001212` |
| `emit`, `stop` | `001240`–`001300` |
| streams A/B/C/D | `002000`/`002040`/`002100`/`002140` |
| external value / assignment target | `003000` / `003002` |
| synthetic frame | `004000` |
| expression stack | `005000` |

The builder rejects unaligned/out-of-24-KB addresses and overlap with the
documented bootstrap at `057744`–`057776`.

## Reproduction and observed results

Generate the manifest and explicit deposits, then run host checks:

```sh
python3 tools/build_stage3a.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -v
```

Each `evidence/stage3a/test-?.simh` starts with
`machines/pdp11/late-summer-1970.simh`, deposits every listed word explicitly,
runs at `001000`, examines final registers/data, and writes a fresh transcript
using SIMH's `SET LOG -N`. No `LOAD` or attachment is used.

| Test | Threaded operation | Observed result |
| --- | --- | --- |
| A | `c;0100; c;1; b12; emit; stop` | printed `A`; HALT PC `001302` |
| B | `x;003000; emit; stop` | printed `B`; HALT PC `001302` |
| C | lvalue `003002/2`; `c;0103; b1; emit; stop` | printed `C`; `003002=000103`; HALT |
| D | `va;4; c;0104; b1; emit; stop` | printed `D`; `004004=000104`; HALT |

The canonical transcripts show an 11/20 with 24 KB, disabled disk/tape
devices and KE, and unattached PTR. The baseline script also reports
`Command not allowed` for redundant `set rha disa` and `set clk ena` commands;
the immediately displayed actual configuration is RHA disabled and CLK
enabled. Stage 3A did not alter that baseline to suppress the diagnostics.

Stage 3A proves only this nucleus. General B conditional/transfer operators,
calls, returns, real frame creation, arguments, and remaining minimal execution
machinery are Stage 3B. Arithmetic expansion, historical assembler/backend,
paper tape/loader, and `dc` remain later gates.
