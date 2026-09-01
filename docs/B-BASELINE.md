# PDP-7 B Baseline

This is the Stage 1 interface record for the B environment on the authoritative
host `machines/pdp7`. File-level evidence is in
[`../evidence/pdp7-b-inventory.tsv`](../evidence/pdp7-b-inventory.tsv).

## Status

**Gate passed.** Static audit, probe design, and native runtime characterization
are complete. Static deductions and observed behavior remain identified
separately below.

## Provenance boundary

- **A:** `scans/bi.s`, `scans/bl.s`, `scans/bc.s`, `scans/ind.b`,
  `scans/lcase.b`, and `scans/op.s` are transcriptions of surviving scanned
  PDP-7 material. `src/cmd/bc.s`, `ind.b`, and `op.s` match those
  transcriptions byte-for-byte.
- **B:** runnable `src/cmd/bi.s` and `bl.s` contain small restoration changes;
  they are not unmodified originals. `bi.s` replaces `ecla lls 4` with
  `cla; lls 4`; `bl.s` normalizes line endings and replaces `sys save` with
  `sys exit` at shutdown.
- **B:** Robert Swierczek's 2016 GPL3 compiler consists of host bootstrap
  `tools/b.c` and self-hosting `src/other/b.b`. The installed `/system/b` is a
  generated executable of that reconstruction, not a Bell Labs compiler
  binary.
- **B:** `hello.b`, `ctype.b`, `string.b`, `brt.s`, `brtb.b`, and `test.b` are
  later reconstruction/example material. The separate `brt` experiment is not
  the default installed runtime path.
- **M:** build recipes, filesystem construction, emulators, static image
  parsing, and new probes are modern instrumentation/convenience.
- **D:** the exact lost Bell Labs compiler source/configuration that produced
  the surviving interpreter's input remains unknown. The Swierczek compiler is
  the working conservative reconstruction used here.

The active and retained-reference trees have identical content for every
B-related file inventoried. Their B environment differs only through the
filesystem images: the active image additionally retains local `shankao`
state. Nothing was replaced from upstream.

## Installed environment and invocation

Read-only filesystem inspection of `image-shankao.fs` establishes:

- `/system/b`: installed compiler, 3,665 PDP-7 words; its decoded word stream
  matches `build/bin/b` word-for-word.
- `/dmr/b.b`, `bi.s`, `bl.s`, and `hello.b`: decoded text matches the checked-in
  runnable/reconstructed sources exactly.
- `/dmr/op.s`: assembler definitions required by the native assembler.
- `/dmr/b_readme`: installed instructions say:

  ```text
  b hello.b hello.s
  as op.s bl.s hello.s bi.s
  a.out
  ```

The compiler therefore takes an input B path and output assembly path. The
native assembler combines opcode definitions, `bl.s` startup/I/O, compiler
output, and `bi.s` interpreter, producing `a.out`, which is then executed.
`/system` is linked into `/dmr`, so `b` and `as` resolve there.

The checked-in `build/fs/b_readme` instead says `bc` and `ops.s`. That seed is
stale relative to the active image: no `/system/bc` exists, `bc.s` is not in
the default build target, and surviving `bc.s` is a diagnostic wrapper around
the B interpreter rather than the Swierczek compiler. Stage 1 uses the
installed `b`/`op.s` procedure and records this discrepancy rather than
rewriting either source.

The `shankao` directory contains `hello.s` and executable `hello`, but static
decoding shows a direct `lac`/`sys write` assembly program. No local `shankao`
B source or saved threaded compiler output was found; these files are not B
probe evidence.

## Static compiler-to-runtime contract

`b.c`/`b.b` emit assembler statements whose leading operator letter selects a
table in `bi.s`. The interpreter fetches an 18-bit word, uses the high four
bits as an operator class, and the low 14 bits as `addr`. Static correspondence:

| Emission | Interpreter entry | Static purpose |
| --- | --- | --- |
| `a n` | `autop` | push address of automatic/parameter at `dp+n` |
| `b n` | `binop` | assignment, Boolean/comparison, arithmetic operator `n` |
| `c n` | `consop` | push small 14-bit constant |
| `f target` | `ifop` | test top value and branch if zero |
| `n n` | `etcop` | call/mark/vector/literal/goto/return/escape suboperation |
| `s n` | `setop` | reset stack to `dp+n` after declarations/expressions |
| `t target` | `traop` | unconditional threaded transfer |
| `u n` | `unaop` | address, negate, indirect, logical-not |
| `x symbol` | `extop` | push external/internal symbol address |
| `y n` | `aryop` | initialize automatic vector base |

`binop` statically contains assignment; OR/AND; equality and ordered
comparisons; add/subtract; remainder/multiply/divide. Shift slots halt in the
surviving runtime and the reconstructed compiler does not emit them. `etcop`
contains the `mcall`, `mark`, `call`, `vector`, `litrl`, `goto`, `retrn`, and
`escp` machinery. `bl.s` supplies `.array`, `.read`, `.write`, `.flush`,
buffering, startup, and shutdown around the interpreter. These relationships
still require observed probes before they become the Stage 1 interface
specification.

## Static unknowns to resolve with probes

- exact emitted sequences and stack cleanup for each representative construct;
- distinction between zero-argument `mcall` and argument-bearing `mark/call`;
- parameter offsets and return-value placement;
- automatic vector initialization versus expression-level indexing;
- external symbol linkage and the callable library surface actually available;
- large literal layout and negative/18-bit behavior;
- comparison truth representation and branch consumption;
- whether the native compiler/assembler invocation behaves exactly as the
  installed note states on the persistent image.

No compiler, runtime, filesystem image, or historical source was changed in
Stage 1A.

## Stage 1B probe design

The probes use names of at most eight characters so they fit the PDP-7
filesystem. Each emits a unique two-character success word through `write` and
an `F` word on failure. Compiler output is retained as the same basename with
`.s`; assembly output is renamed before the next probe so `a.out` is not
silently reused. Expected operations below are predictions from static source,
not observed results.

| Probe | Purpose and expected observation | Uncertainty resolved | Later decision depending on it |
| --- | --- | --- | --- |
| `pconst.b` | Small `7` should emit `consop` (`c`); `020000` and negative `-3` should expose literal encoding (`n 5` plus word where needed); execution prints `C1`. | Small/large/negative constant boundary and truth composition. | Constant cells and 18-bit literal representation in a later threaded target. |
| `pstore.b` | Autos should emit `autop`; assignments `binop` assignment; reads should reveal indirection/lvalue handling; execution prints `S2`. | Stack slot offsets, load versus address semantics, expression cleanup via `setop`. | Target stack frame and load/store operator contract. |
| `parith.b` | Output should select add, subtract, multiply, divide, and remainder `binop` slots; execution prints `A3`. | Operand order, quotient/remainder behavior, and actual EAE-backed runtime path. | Which arithmetic operators later require target support or software substitutes. |
| `pbrnch.b` | All six comparisons should select their `binop` slots and each `if` should emit `ifop` plus labels/transfers; execution prints `B4`. | True value, signed ordering, and conditional-branch stack behavior. | Comparison and branch interface for later threaded operators. |
| `ploop.b` | Compiler should emit a loop label, `ifop` exit, and unconditional `traop`/goto path; execution prints `L5`. | Backward transfer encoding and per-iteration stack reset. | Control-flow layout and branch relocation requirements. |
| `pcall.b` | Zero-argument call should emit `mcall`; `retrn` should return value `7`; execution prints `C6`. | No-argument frame creation, saved PC/DP, return-value placement. | Minimal call/return machinery and frame layout. |
| `pargs.b` | Two-argument call should emit `mark`, argument expressions, `call`, parameter autos, and `retrn`; execution prints `G7`. | Parameter order/offsets, argument copying, cleanup, returned value. | Argument-bearing call operator and ABI-like stack contract. |
| `pvec.b` | `auto v 3` should emit `aryop`; indexing should emit `vector`; `&`/`*` should emit address/indirect `unaop`; execution prints `V8`. | Vector base initialization, indexing units, address and indirect semantics. | Target vector representation and indirection operators. |
| `pext.b` | Explicit `extrn write` should emit `extop` naming `.write`, followed by argument-bearing call machinery; execution prints `E9`. | External symbol spelling/linkage and library entry calling convention. | Runtime-library boundary and external relocation/linkage rules. |

For every probe Stage 1C must capture: source hash, compiler exit/diagnostics,
complete emitted `.s`, assembly outcome, executable outcome, and exact console
text. A failure is recorded before any repair. The probes intentionally avoid
shifts because the surviving `bi.s` shift entries halt and the reconstructed
compiler grammar does not emit shift operators.

## Stage 1C first-run record

The authoritative PDP-7 was booted from `image-shankao.fs`; no PDP-11 process
was started. Startup reported `set ptr ena` and `set ptp ena` as `Command not
allowed`, although `show dev` still reported PTR device 01 and PTP device 02
present and both remained unattached. Those two invalid explicit directives
must be removed after the session; fresh-process unattached defaults remain the
observed reproducible state.

Probe sources were entered as new files without replacing compiler/runtime
sources. Console UNIX translation lowercased typed alphabetic literals, so
success words appear lower-case. First observed outcomes, recorded before any
probe refinement:

| Probe | Compiler result | Native assembly/runtime result | Significance |
| --- | --- | --- | --- |
| `pstore.b` | clean | native `as op.s bl.s pstore.s bi.s`; prints `s2` | `autop`, assignment/load, add, equality, `ifop`, external argument call work end to end |
| `pbrnch.b` | clean | native assembly; prints `b4` | all six comparison slots and repeated conditional branches work |
| `ploop.b` | clean | native assembly; prints `l5` | backward transfer, loop exit, and repeated `setop` work |
| `pargs.b` | clean | native assembly; prints `g7` | `mark`/argument expressions/`call`/parameter access/`retrn` work |
| `pext.b` | clean | native assembly; prints `e9` | explicit `extrn write` resolves to `.write` and calls through `bl.s` |
| `pconst.b` | diagnostics `sz 6`, `sx 7`, repeated `sz 7` | not assembled/run | later image extraction proved this console transfer was oversized/corrupt; not a compiler limitation |
| `parith.b` | analogous `sz`/`sx` diagnostics | not assembled/run | later image extraction proved this console transfer was oversized/corrupt; not a compiler limitation |
| `pcall.b` | `ex 5`, `sz 8`, `ex 8`, `() 8`, `sz 9` | not assembled/run | later image extraction proved this console transfer was oversized/corrupt; zero-argument call still requires a valid rerun |
| `pvec.b` | `[] 6`, `xx 6`, `ex 6`, `sz 7`, `xx 8` | not assembled/run | later image extraction proved this file was truncated; not a compiler limitation |

The corrupt sources and their failed generated files are retained in the
persistent image as transfer-failure evidence. Their word counts do not match
the reviewed sources (`pext.b` is empty and `pvec.b` is truncated). No
compiler or runtime repair was attempted.

After recording those failures, four new isolation probes were designed:

- `pcnst2.b` replaces the three-way constant predicate with three separate
  comparisons and an `ok` count; this distinguishes literal handling from
  expression-depth/parser synchronization.
- `parth2.b` similarly validates each arithmetic result separately; it keeps
  the same operator coverage while removing the long Boolean expression.
- `pvec2.b` tests only automatic vector allocation/indexing (`aryop` and
  `vector`).
- `pind.b` tests address-of and indirect assignment on a scalar (`uadr` and
  `uind`) without vector indexing.

Expected success words remain `c1`, `a3`, `v8`, and `i8` after console
lowercasing. These are probe refinements, not compiler/runtime repairs.

All four refinements passed natively (`c1`, `a3`, `v8`, `i8`). A synchronized
replacement of the corrupted zero-argument call probe also passed (`c6`). The
ten valid emissions and their hashes are preserved under
`evidence/pdp7-b-stage1/generated/`; the failed transfers are separately
preserved under `evidence/pdp7-b-stage1/corrupt/`. Exact inode, size, hash, and
observed-output records are in `evidence/pdp7-b-stage1-results.tsv`.

The initial queued/corrupt attempts were made in `/shankao`; the ten final
valid captures were compiled, assembled/linked, and executed in `/dmr` after
ownership/linking restrictions obstructed the intended `shankao` workflow.
This account choice supplied the existing local runtime/linkage context but
does not affect the compiler/runtime behavior characterized here. It is a
workflow caveat, not a reason to rerun or reinterpret the evidence.

## Observed compiler/runtime interface

The valid probes establish this interface to the surviving interpreter in
`bi.s` and threaded operation table in `op.s`:

- Functions are emitted as `.name:.+1`, followed by `s N`. Automatic slot
  numbering begins at 2; parameters and automatic scalars use frame offsets.
- `a N` pushes an address. Binary operators dereference operands as required;
  assignment is `b1`. `s N` establishes the frame and resets temporary state.
- Nonnegative constants through octal `017777` use `c`; full-word values,
  including negatives and `020000`, use `n5` followed by the word.
- Binary slots observed are assignment 1, AND 3, equality 4, inequality 5,
  `<=` 6, `<` 7, `>=` 8, `>` 9, addition 12, subtraction 13, remainder 14,
  multiplication 15, and division 16. Comparisons produce true as 1.
- Conditional control uses `f label`, branching on zero. The compiler's
  unconditional path is `x label; n6`; no direct `t` emission was observed.
- Zero-argument calls use `x .callee; n1`. Calls with arguments use
  `x .callee; n2`, argument expressions, then `n3`. The two-argument probe
  reads parameters through `a2` and `a3`. Return is `n7`; the compiler also
  appends a default `n7` at function end.
- `auto v[3]` emits `y2` and expands the frame to `s6`. Vector indexing emits
  base address, index expression, and `n4` (`aryop`).
- Scalar address-of emits its address followed by `u1`; indirect access emits
  the pointer address followed by `u3`. Indirect assignment then uses `b1`.
- `write(...)` emits `x .write; n2`, its argument, and `n3`. Native linkage is
  reproducibly `as op.s bl.s emitted.s bi.s`; `bl.s` supplies library symbols.

This covers `consop`, `binop`, `setop`, branches, calls, vectors/indirection,
and an external call, establishing:

`B source -> reconstructed /system/b -> emitted threaded assembly -> native as
+ surviving bi.s/bl.s runtime -> observed execution`.

## Limits and retained uncertainty

- Four first-pass console transfers were corrupted; synchronized editor input
  was used for valid replacements. These are transfer failures, not B failures.
- The host reconstructed compiler needs `gcc -std=gnu89` with the current GCC;
  native `/system/b` is the compiler characterized here.
- Shift slots halt in the surviving runtime and no compiler shift syntax was
  demonstrated; shifts are outside the observed supported subset.
- `.write` is the dynamically exercised library boundary. Other `bl.s`
  routines remain statically inventoried rather than behaviorally specified.

No compiler or runtime source was changed during characterization.
