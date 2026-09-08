# PDP-7 `as11` reconstruction

## Scope and evidence boundary

Participant accounts establish that a simple PDP-11 assembler was written in
B and run on the PDP-7, making a two-pass B tool historically plausible. The
exact 1970 source and language are lost. Stage 4 reconstructs the tool as class
**B** in five dependency gates; this document records completed Stages 4A and
4B and the remaining plan.

Local recovered/restored sources under `machines/pdp7/pdp7-unix/src/` are the
implementation evidence used here: `cmd/bl.s` for B I/O, `sys/s2.s` for
`seek`, and `cmd/as.s` for authentic PDP-7 assembler seek use. No web research
or third-party import was needed.

## Stage 4A — two-pass I/O substrate

Stage 4A isolates kernel seeking, B buffering, EOF, and textual output before
any assembler parser, symbol table, or PDP-11 encoder exists.

### Buffered input and rewind

Recovered `bl.s` implements `.read` through `getc`. `iflg` holds the pending
low 9-bit character from a fetched PDP-7 word; `getc` returns and clears it
before considering the buffer pointers. When `cibufp == eibufp`, `getc` reads
up to 64 words (128 characters) from `.fin` into `ibufp`, then sets
`cibufp = ibufp` and `eibufp = ibufp + words_read`. A nonpositive kernel read
returns octal `004` to B as EOT/EOF.

Seeking only the descriptor would leak a pending character or unread old
buffer data. The separate class-B helper is
[`rewind.s`](../src/pdp7/as11/rewind.s). It performs exactly:

```text
lac .fin
sys seek; 0; 0       absolute character offset zero
...                  stop on negative seek result
dzm iflg             discard pending second character
lac eibufp
dac cibufp           invalidate current range
jmp fetch            return to B threading
```

`ibufp` and `eibufp` are not rewritten. Making the current pointer equal to
the end pointer forces the next `getc` through its existing refill path. The
helper uses the no-argument B-callable prologue style of `.flush` and does not
modify shared `bl.s`.

### Native test

[`io_probe.b`](../tests/pdp7-as11/io_probe.b) ran with a deterministic
378-character lowercase input. Lowercase avoids observed PDP-7 tty case
translation. All reads, comparisons, EOF handling, rewind calls, octal
conversion, and flushing executed inside PDP-7 UNIX/B as `shankao`.

| Case | Boundary | Observed result |
| --- | --- | --- |
| A | odd 17-character mid-buffer prefix | A1 and A2 prefixes identical |
| B | 173 characters, crossing 128-character refill | B1 and B2 prefixes identical |
| C | read whole input | EOF `000004`; count `000572` octal = 378 |
| C restart | rewind after EOF | first 17-character prefix repeated exactly |
| octal | B `putoct6` plus `.write`/`.flush` | `000000`, `000001`, `077777`, `100000`, `177777` exactly |

The canonical 472-character output and native session are under
`evidence/stage4a/`. The first transfer/link failure and diagnosis are retained
there as well.

### Machine and provenance policy

The corrected gate ran directly on authoritative evolving `machines/pdp7`,
not a disposable image. The class-M runner logged in as `shankao`, retained a
native same-directory `s4op.s` copy, installed checked-in `bl.s`/`bi.s` text as
shankao-owned `s4bl.s`/`s4bi.s`, paced terminal transfers, built with native
`b` and `as`, and compared output deterministically. Shared originals were
neither edited nor chowned.

The final run changed `image-shankao.fs` from SHA-256
`ee3b12de0b1d6ac304237bcbb2424759eb06870ff72b5cdae56c6032248b9c07`
to `ab6494ab9c3f786544533ff2cd9a054e639f64d8e5095eb4473bd4c965e6cab0`
by replacing Stage-4A-owned sources, generated `io.s`/`a.out`, input, and
result in `shankao`. Earlier discovery/failure sessions also evolved the image;
no legitimate state was restored to retain an old hash. The Stage 4A follow-up
checkpoint committed this authoritative image after `fsck7` completed without
a consistency warning.

The runner and session capture are class **M**. They automate observed PDP-7
behavior; they do not implement rewind semantics on the host.

## Stage 4B — language and symbol engine

[`as11.b`](../src/pdp7/as11/as11.b) is the class-B semantic front end. It has
no PDP-11 opcode/addressing table and emits no machine code. Native invocation
as `shankao` is:

```text
b as11.b as11.s
as s4op.s s4bl.s as11.s rewind.s s4bi.s
a.out source result
```

The first two commands compile/link with shankao-owned runtime copies. The
last executes pass 1, calls Stage 4A `rewind`, and rereads the same descriptor
for pass 2. The complete source is never stored in memory.

### Frozen language contract

Space and tab separate tokens. Physical newline terminates a statement and
increments the line number; semicolon terminates a logical statement without
incrementing it. Slash discards everything, including semicolons, through
physical newline. B EOT `004` is EOF. The scanner uses one-character pushback.

Identifiers begin with a letter/underscore and continue with letters, digits,
or underscore. Characters are compared exactly and `as11` does not case-fold;
fixtures are lowercase because the configured transfer path lowercases input.
The complete legal spelling is consumed, but only eight characters are packed
and significant. Thus `longnamex` and `longnamey` identify the same symbol.

Numbers are octal sequences containing only `0`–`7`; ordinary 8/9 constants
are rejected. Decimal and hexadecimal are absent. A single digit `0`–`9`
followed by `:`, `f`, or `b` is a numeric-local construct. Expressions contain
octal numbers, globals, numeric locals, `.`, unary minus, binary `+`/`-`, and
square-bracket grouping. Binary operations evaluate left-to-right; brackets
override. Parentheses and all broader arithmetic/relocation syntax are absent.

`.` is a future PDP-11 **byte** address. A bare expression models one future
16-bit word and advances `.` by two; odd addresses fail. `.=expr` requires an
immediately resolved `000000..177777` address. A fixed-size bare word may
forward-reference a label in pass 1 but must resolve in pass 2. Semantic word
values use `&0177777`, so `-1` becomes `177777`; positive word overflow and
address overflow fail.

### Symbols and passes

Each global entry is six PDP-7 words: four words packing two 9-bit characters
each, a state, and a value. The 64-entry `gtab[384]` supports undefined, label,
and assigned states. A label resolves an undefined entry; duplicate labels and
label/assignment conflicts fail. Assigned values must resolve immediately and
may be reassigned. Pass 2 checks label values against pass 1 and has a real
phase-error path; final undefined symbols fail.

Numeric locals are separate: ten occurrence counters plus 64 two-word
digit/occurrence-key and address entries in `ltab[128]`. Counters reset on each
pass. Repeated definitions, forward `nf`, and most-recent backward `nb` work;
missing directions fail.

Pass 2 emits lowercase semantic records only:

```text
l <name> <address>
a <name> <value>
n <digit> <address>
w <address> <value>
```

Addresses/values are six-digit octal. Errors are
`e <six-digit-physical-line> <two-character-code>`.

### Native results and resources

The 456-byte positive fixture covers required scanner, symbol, assignment,
expression, comment/semicolon, local, long-name, location, and cross-refill
behavior. Empty/comment-only input succeeds. The 604-byte substantial fixture
uses 48 globals and 10 numeric definitions and emits 58 words. Thirteen
negative fixtures reject all required error classes. A production phase check
exists; no artificial phase inconsistency fixture was added.

Local Stage 3 measurement finds 17 globals and 5 numeric definitions. Native
`stat` reports:

| Artifact | PDP-7 words | Octal |
| --- | ---: | ---: |
| `as11.b` | 4,414 | `010476` |
| generated `as11.s` | 5,879 | `013367` |
| linked `a.out` | 3,301 | `006345` |

Against the ordinary 4,096-word user region, linked-file size leaves about 795
words (`01433`) of static load-size headroom. This is a file-size estimate,
not a live stack high-water mark. Compact tables consume 522 words. Ordinary B
was sufficient; Virtual B and host-side symbol processing were not used.

All native work ran as `shankao`; authentic shared files were unchanged. The
class-M runner only transfers, supervises, captures, and compares fixed output
hashes. The final image SHA-256 is
`3543d5a5e055072c9c99af0204a01479caa62b62442dc84b8c08d2631dad4c5a`.
See `evidence/stage4b/` for traces, diagnostics, and checkpoint details.

## Stage 4C — KA11 encoding (complete)

Local Stage 3 sources require exactly `add asl asr bne bpl br clr cmp halt
jmp mov movb tst tstb`; `movb`/`tstb` are byte forms and `br`/`bne`/`bpl`
are branches. Stage 4C also adds JSR and RTS because their encoding classes
and bootstrap value are small. No other mnemonic is accepted; in particular
`mul div ash ashc xor sob mark` remain ordinary identifiers or errors, and
the threaded-runtime symbol `mark` remains usable as a raw expression.

The B operand parser accepts `r0`–`r5`, `sp`, `pc`, `(r)`, `(r)+`, `*(r)+`,
`-(r)`, `*-(r)`, `expr(r)`, `*expr(r)`, `$expr`, `*$expr`, `expr`, and
`*expr`. It records 0/no extension, 1/absolute extension, or 2/PC-relative
extension. Source extensions precede destination extensions. For an extension
at E, PC-relative output is `target-(E+2)`. Byte instructions still emit full
16-bit extension words. JMP/JSR register-mode destinations are rejected.

Branch byte delta is `target-(A+2)`, checked against `-0400..0376` before
division. Because native B negative division did not have the initially
assumed behavior, the implementation divides a positive magnitude and restores
the sign. Native `-0200` and `0177` word-displacement boundaries pass; `-0201`,
`0200`, and odd targets fail. Pass 2 emits `i` instruction, `x` extension, and
existing `w` raw-word records.

The fixed native encoding trace contains 30 oracle-decodable instructions and
matches the Stage 2 vectors across all eight modes, PC-special modes, dual
extensions, bytes, branches, JMP, JSR, RTS, and every Stage 3 mnemonic. All 18
new negative fixtures pass, as does the normal Stage 4B positive fixture.

### Ordinary-B capacity finding

The linked artifact is 3,696 words (`007160`),
from 5,636-word `as11.b` (`013004`) and 8,217-word generated `as11.s`
(`020031`). `bl.s` reserves the top 128 words for input/output buffers. To
avoid charging unused capacity to the executable, the current reconstruction
stores up to 48 five-word globals downward from `017537` and ten two-word
numeric locals at `017544..017567`; state occupies otherwise-unused high bits
of the first packed ASCII name word. This remains native B processing.

At the measured maximum (48 globals, 10 locals), the lowest global begins at
`017164`, while the executable's upward-growing B stack begins at `017160`.
Only five words remain, and the 604-byte Stage 4B substantial fixture exits
with an empty result. The informative attempts and all successful partial
results are retained in `evidence/stage4c/`.

### Capacity characterization

The linked file is loaded at user address `010000`. Its `007160` words end at
`017157`, which is also `bi.s`'s final `stack` word; `sp`, `dp`, and `ap` are
initialized to that label, and interpreter operations grow `sp` upward. The
first global entry begins at `017537`; subsequent five-word entries grow
downward. Ten two-word numeric-local entries grow upward through
`017544..017567`. Independently, `bl.s` lowers `lastv=017770` twice by 64 words
at startup, so its output and input buffers occupy `017570..017767` above the
local table.

Thus the earlier five-word figure is the count of addresses from the B stack
label `017157` through `017163`, immediately below the lowest 48th global at
`017164`. It is not measured dynamic stack headroom. With so little room,
pass-1 calls overwrite stack/control state and the process can exit before
`flush()`, leaving the already-created output file empty. At a less severe
collision (39 globals plus locals), execution survives long enough for pass 2
to observe overwritten pass-1 symbol state and emit `e 000051 ph`.

Native boundary tests preserve exact semantic traces through 38 globals and
10 local definitions (55-word static separation). Thirty-nine globals pass
only with zero locals; adding even one local fails, so 39/0 is not a safe
general capacity. A realistic 646-byte Stage-3-shaped input using all Stage 3
mnemonics, 17 globals, and five local definitions passes and produces a
1,249-byte trace decoded by the Stage 2 oracle. Its static separation is 160
words—105 more than 38/10. All Stage 4B constructs used by the stress family
remain correct below the boundary. This is therefore a capacity regression,
not a semantic regression.

One investigated clean guard was to change the native global allocation
limit from 48 to 38, retaining the existing `gf` error before allocating a
39th entry. It should require only an immediate-literal replacement (no linked
growth) and executes wholly on PDP-7. It is proposed, not yet implemented or
accepted or implemented. A dynamic `sp` guard would require a B-callable runtime
hook and reserve for the guard's own call, adding roughly 10–20 words and more
uncertainty.

Source inspection found only modest low-risk savings: factoring duplicate
value/range checks may save roughly 5–10 words; merging trace-output prefixes
may save roughly 5–12 words but increases coupling. Removing JSR/RTS could save
their six table words plus a small dispatch arm, but would discard explicitly
tested bootstrap support and is not recommended. Removing semantic trace
records could save more (roughly 40–80 words), but would first require a new
deterministic validation path. None of these estimates has been encoded or
measured by rebuilding. See `evidence/stage4c-capacity/`.

The completed-stage interpretation separates concerns deliberately. Stage 4B
guarantees its language/parser/symbol semantics and records that standalone
implementation's 48/10 stress result; it does not promise that every larger
successor executable retains the same maximum. Stage 4C guarantees those
semantics remain available, the KA11 encoder is correct, and the current
Stage-3-shaped 17/5 bootstrap workload fits with substantial margin. The
Unix-driven `as11` completion gate owns the final textual object map, combined
bootstrap-sufficient capacity, clean exhaustion behavior, and documented
safety margin. This preserves the
48/10 evidence without turning it into the wrong substage gate. Stage 4C is
therefore **COMPLETE/PASS**; the allocator, capacities, encoder, and trace were
not changed to close it.

## Completed labels and remaining named gates

- **4B: complete.** Language, tokenizer/parser, and two-pass symbol/local-label
  engine; no target encoding.
- **4C: complete.** KA11 encoding and current bootstrap-shaped feasibility are
  independently verified; the measured capacity frontier remains evidence.
- **Unix-driven `as11` completion:** finalize the textual map and establish
  guarded, bootstrap-sufficient integrated capacity and safety margin.
- **Stage-3 gold round trip: complete.** The readable Stage-3B test-L fixture
  is assembled by PDP-7 B `as11`; class-M tooling parses its 110 native
  `i`/`x`/`w` words, verifies them against the Stage-2-backed Stage-3 manifest,
  deposits those exact words, and observes `D` on the PDP-11/20. The host does
  not encode or replace instructions.

Stage 4C is complete; the Unix-driven `as11` completion gate has not started.
Its implemented mnemonic set is a validated encoder nucleus and B-bootstrap
test corpus derived from Stage 3, not the final historical requirement for
`as11`. The provisional v1 PDP-7 UNIX migration corpus is now frozen in
[`UNIX-MIGRATION.md`](UNIX-MIGRATION.md). The completion gate will choose
additional instructions or directives from that real workload and judge final
capacity against selected bootstrap/migration inputs rather than assembler
completeness or the Stage-3 corpus alone.
