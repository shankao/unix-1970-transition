# PDP-11 threaded-B runtime reconstruction

## Scope and provenance

Stage 3 was split because the direct-threaded nucleus has unusually strong
technical evidence while the late-1970 control, call, return, and frame
machinery is less certain. **Stage 3A** reconstructed and executed the
strongly evidenced nucleus; **Stage 3B** then reconstructed and demonstrated
the remaining control and call machinery. Both gates, and overall Stage 3,
are complete.

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

At the Stage 3A checkpoint this proved only the nucleus; the conditional,
call, return, frame, and argument work was deliberately deferred to Stage 3B
below. Arithmetic expansion as needed by applications, the historical
assembler/compiler, paper tape/loader, and `dc` remain later gates.

## Stage 3B control and call reconstruction

Stage 3B adds class-B `f` (branch on zero), `tra` (unconditional threaded
transfer), `b4` (equality), `mark`, `call`, `set`, automatic-rvalue `a`,
return-without-value `n11`, and return-with-value `retv`. CPU branches inside
fragments are implementation details; B control targets are byte addresses in
the threaded stream. `f` consumes its value: zero loads its following target
into R3, while nonzero skips that target word. `tra` always loads it.

The call entry is reconstruction, not printed Thompson source. It follows the
Stage 1 compiler order exactly: function value, mark, left-to-right argument
expressions, call. `mark` removes the function value and reserves a frame at
the current R5 while leaving R4 unchanged so argument operators still address
the caller. R2 temporarily holds this pending-frame address. `call` replaces
the temporary callee word with caller R3, activates R4, and dispatches to the
callee. R2 is not the B stack and has no persistent frame role.

The active frame is:

| Byte offset / B slot | Meaning |
| --- | --- |
| `0` / word 0 | previous R4 |
| `2` / word 1 | saved caller R3; replaced by a returned value on unwind |
| `4` / word 2 | first argument/automatic |
| `6` / word 3 | second argument/automatic |
| later words | additional arguments/automatics/expressions |

Arguments are stored left-to-right beginning at byte offset 4, agreeing with
the Stage 1 `pargs.s` use of automatic slots 2 then 3. `set N` moves R5 to
`R4 + 2*N`; `a offset` loads an automatic rvalue. This hand stream separates
`a` from the documented `va` lvalue operator rather than changing `va`.

For the canonical calls, caller R5 begins at `005000`; mark makes that the
callee frame base. After a value return, the result is at `005002` and R5 is
`005004`; the caller's `emit` consumes it and leaves R5 `005002`. One- and
two-argument values remain visible at `005004` and `005004`/`005006`
respectively. These locations are fixed test placement, not historical
addresses.

Archaeological `n11` is retained materially unchanged:

```text
mov r4,r5; mov (r5)+,r4; mov (r5),r3; jmp @(r3)+
```

Thus void return leaves R5 at frame word 1. `retv` first saves the callee's
top value, performs the same unwind, overwrites saved-R3 word 1 with the value,
advances R5 to word 2, and dispatches through the recovered R3. This convention
is inferred from the documented frame, Stage 1 observed return behavior, and
the local PDP-7 `retrn` fragment; it is not claimed as recovered 1970 source.

### Stage 3B observed tests

The fixed M-class placement keeps streams at `002200`–`002600`, functions at
`003100`–`003340`, the expression/call frames at `005000` upward, and the
synthetic return frame at `006000`. It remains inside 24 KB and clear of the
bootstrap.

| Test | Capability | Bare-machine result |
| --- | --- | --- |
| E | nonzero conditional plus threaded transfer | `E`, HALT |
| F | zero conditional target | `F`, HALT |
| G | repeated loop, equality, assignment | `123`; counter `000064`; HALT |
| H | synthetic archaeological `n11` | `H`; R4 `004000`, R5 `006002`; HALT |
| I | one argument/identity return | `A`; slot 2 `000101`; HALT |
| J | two arguments and `b12` return | `B`; slots 2/3 `000100`/`000002`; HALT |
| K | explicit returned value | `C`; caller result slot `000103`; HALT |
| L | nested outer/inner calls | `D`; two-frame chain observed; HALT |
| M | real call and void `n11` return | `V`; HALT |

Nested test L leaves outer frame word 0 at `005000 = 004000` and inner frame
word 0 at `005006 = 005000`. Inner argument slot `005012 = 000001`; the inner
result at `005010` becomes `000104`, then the outer result appears at caller
slot `005002`. Both frames unwind to R4 `004000` and R5 `005002` after emit.

The first G run printed only `1`: reconstructed `b4` executed CLR before BNE
and destroyed CMP flags. The failure transcript is retained; `b4` now branches
on CMP flags before constructing 0/1. No evidenced operator was changed.

Stage 3A A/B/C/D scripts were rerun unchanged and remain passing. Stage 3B
does not implement the complete B operator library, multiplication/division,
general shifts, vectors, a historical assembler/backend, or loading/tape.
Those remain separately gated.
