# Dependency-Gated Project Plan

## Purpose

This plan is deliberately designed to expose failure points early. The target is not to discover architectural problems after hours of interactive emulator work.

Each stage has:

- **Inputs** — what must already exist.
- **Work** — what we intend to build or establish.
- **Evidence boundary** — what is historical versus reconstructed.
- **Gate** — a concrete condition that must pass before continuing.
- **Fallback** — what we do if the gate fails.

---

## Stage 0 — Freeze and record the machines

**Status: COMPLETE**

### Inputs

Working PDP-7 UNIX host and bare PDP-11/20 emulator.

### Work

Record exact SIMH versions/configuration, disk image hashes, enabled devices, memory size, and any hand-deposited memory.

### Evidence boundary

The emulator and configuration scripts are modern machinery. The configured hardware should represent the historically intended machine state.

### Gate

Both machines can be recreated from documented configuration without relying on chat history.

### Fallback

Do not modify either machine until reproducibility is restored.

---

## Stage 1 — Characterize the existing PDP-7 B environment

**Status: COMPLETE**

### Inputs

The currently working PDP-7 B reconstruction plus surviving PDP-7 B runtime/interpreter material.

### Work

Use a small fixed probe corpus to determine the actual interface between B source, compiler output, interpreter/runtime operators, symbols, storage, calls, branches, and vectors.

Suggested probes:

- integer constant
- addition/subtraction
- multiplication if supported
- assignment
- `if`
- loop
- function call/return
- vector indexing
- external/library call

### Evidence boundary

Surviving PDP-7 source/listings are class A. Reconstructed B compiler pieces remain class B and must not be relabelled as original.

### Gate

Produce a checked-in document/test fixture mapping each probe from B construct to emitted/interpreted representation well enough to retarget the backend.

### Fallback

If the current B reconstruction is too opaque or divergent, isolate a smaller supported B subset and explicitly make that the input language of the transition reconstruction.

---

## Stage 2 — Build a modern verification oracle

**Status: COMPLETE**

### Inputs

PDP-11 instruction documentation and known test vectors.

### Work

Create host-side tooling that can independently:

- encode/decode the PDP-11 instruction subset we use;
- calculate and invert branch displacements;
- handle instruction extension words and little-endian bytes;
- compare later PDP-7-generated words with expected PDP-11 words.

Threaded-B stream inspection belongs with the reconstructed runtime boundary;
paper-tape records/checksums remain gated to Stage 7 and are not silently
selected here.

### Evidence boundary

Everything in this stage is class M. It is instrumentation only and must not appear in the final historical execution path.

### Gate

Independent KA11 instruction vectors encode/decode reproducibly, later/EIS
instructions are rejected, and the documented bootstrap is walked correctly.

### Fallback

Use an existing trustworthy assembler/decoder as a temporary oracle, but pin its version and keep it outside the historical path.

---

## Stage 3 — Reconstruct a minimal standalone PDP-11 threaded-B nucleus

**Status: IN PROGRESS — Stage 3A COMPLETE; Stage 3B NEXT**

### Inputs

Ritchie's description of B threaded execution; authentic PDP-7 interpreter semantics; later binary-derived PDP-11 B runtime archaeology.

### Stage 3A — strongly evidenced execution nucleus

**Status: COMPLETE**

Reconstruct the documented R3/R4/R5 direct-threaded architecture and the
`c`, `x`, `va`, `b12`, and `b1` fragments. Use fixed class-M deposits to prove
constant/addition, external rvalue, assignment word-address scaling, automatic
lvalue scaling, direct console output, and clean halt on the bare target.

**Gate:** four streams emit A/B/C/D; assignment leaves `0103`; synthetic-frame
automatic leaves `0104`; only base KA11 instructions and volatile deposits are
used.

### Stage 3B — remaining minimal execution machinery

**Status: NEXT — NOT STARTED**

### Work

Implement only the operator fragments necessary for first execution:

- general threaded control/branch operators
- call/return
- real frame setup and argument handling
- any remaining operators needed by the minimal Stage 3 program

Initially assemble this with modern tooling so target-runtime debugging is isolated from cross-assembler debugging.

### Evidence boundary

The exact diskless-1970 PDP-11 runtime is lost. This implementation is class B, informed by class A accounts and later archaeological material.

### Stage 3B gate

A hand-constructed representative stream exercises the reconstructed control,
call/return, frame, and argument boundary on the bare PDP-11 with verified
state/output and no operating system.

### Fallback

Keep Stage 3B open and reduce the next test to the smallest unresolved control
or frame boundary. Do not reinterpret the proven Stage 3A nucleus or advance
to later stages to compensate.

---

## Stage 4 — Audit PDP-11/20 arithmetic

**Status: NOT STARTED**

### Inputs

Minimal runtime from Stage 3 and confirmed PDP-11/20 hardware configuration.

### Work

Determine which operations require software implementation because the base PDP-11/20 lacks later EIS instructions and because KE11 availability at Bell Labs is not established.

Implement, as needed:

- multiply
- divide/remainder
- multi-bit shifts

### Evidence boundary

Do not silently enable optional hardware to make later code work.

### Gate

Threaded-B integer arithmetic tests pass with the configured machine and no undocumented hardware assumption.

### Fallback

Constrain the first B subset further, document the limitation, and continue historical research into the Bell Labs hardware order/configuration before expanding it.

---

## Stage 5 — Reconstruct the PDP-7-hosted PDP-11 assembler

**Status: NOT STARTED**

### Inputs

Working PDP-7 B environment; modern PDP-11 oracle; known assembly subset required by runtime/backend.

### Work

Write a deliberately small assembler in B that runs on the PDP-7. It should support only what the reconstructed historical toolchain needs, for example:

- labels/symbols
- numeric constants/words
- required PDP-11 opcodes
- required addressing modes
- branches
- `JSR` / `RTS`
- minimal directives

Avoid recreating PAL-11 unless evidence requires it.

### Evidence boundary

The historical B-written assembler is attested but its source appears lost. This implementation is class B.

### Gate

The PDP-7 assembler matches the independent oracle byte-for-byte over a meaningful regression corpus.

### Fallback

Shrink the accepted assembly grammar to exactly the compiler output we need. Complexity in a lost general assembler is not a goal.

---

## Stage 6 — Reconstruct the PDP-7 B-to-PDP-11 backend

**Status: NOT STARTED**

### Inputs

Characterized PDP-7 B front end/runtime model; working reconstructed `as11`; standalone PDP-11 threaded runtime.

### Work

Produce the PDP-11-target form expected by `as11`. Prefer to preserve the structure of the working PDP-7 B reconstruction where evidence permits rather than inventing a new compiler architecture.

### Evidence boundary

Ritchie explicitly records a PDP-7 B cross-compiler for the PDP-11. Exact source/output conventions are lost. Later B reconstruction work is evidence/reference, not proof of exact 1970 implementation.

### Gate

A small B program compiled on the PDP-7 yields threaded PDP-11 output that agrees with independently constructed expected sequences.

### Fallback

Define and document a historically plausible restricted B subset. Do not add modern language conveniences merely to make examples easy.

---

## Stage 7 — Establish the general paper-tape path

**Status: NOT STARTED**

### Inputs

PDP-7-generated PDP-11 object bytes; PDP-7 paper-tape punch; PDP-11 reader; contemporary DEC loading documentation.

### Work

Determine whether further evidence identifies Bell Labs' exact tape encoding. If not, adopt a contemporary DEC loading format as an explicit class C substitute.

The likely practical path is:

```text
14-word bootstrap
    -> larger loader
    -> arbitrary-size program records
```

The PDP-7 must generate/punch the final program tape itself for the historical demonstration.

### Evidence boundary

Paper-tape transfer is historically attested. Bell Labs' exact byte/record format is currently unknown. A DEC format must be labelled as a substitute unless evidence changes that.

### Gate

A tape image produced by PDP-7 execution is attached unchanged to the PDP-11 reader, loads successfully, and starts a known program.

### Fallback

If no general contemporary loader can be made to fit the period and hardware, reconstruct a minimal loader but mark both loader and format class B rather than inventing undocumented Bell Labs provenance.

---

## Stage 8 — Prove the complete historical-style loop

**Status: NOT STARTED**

### Inputs

Stages 1–7 passing.

### Work

Run the entire loop without modern code generation in the path:

```text
B source on PDP-7
 -> PDP-7 B-to-PDP-11 compiler/backend
 -> PDP-7 B-written PDP-11 assembler
 -> PDP-7 paper-tape punch
 -> tape image
 -> PDP-11 reader/loader
 -> standalone threaded-B runtime
 -> visible result
```

Modern scripts may automate emulator attachment/detachment and verify output, but may not alter the program tape.

### Gate

Edit a B source file on the PDP-7, rebuild it there, repunch, transfer, and observe the changed behavior on the PDP-11.

### Fallback

The first failing boundary becomes a separately reproducible issue/test. Do not debug the whole pipeline interactively.

---

## Stage 9 — Build a small calculator systems test

**Status: NOT STARTED**

### Purpose

Before attempting `dc`, stress the exact categories `dc` will require without introducing arbitrary precision immediately.

### Work

Implement a small integer RPN calculator in the reconstructed B subset, including:

- token input
- operand stack
- `+ - * /`
- print top
- basic error handling if feasible

### Gate

Repeated interactive calculations work on the bare PDP-11 using the complete PDP-7 development/tape loop.

### Fallback

Fix the runtime/compiler/loader boundary exposed by the calculator. Do not start arbitrary precision yet.

---

## Stage 10 — Reconstruct a historically grounded early `dc`

**Status: NOT STARTED**

### Inputs

Stable Stage-9 calculator and accumulated evidence about early `dc` behavior.

### Work

Reconstruct incrementally:

1. RPN parser and stack discipline.
2. Multi-precision number representation.
3. addition/subtraction.
4. multiplication/division.
5. print/scale behavior justified by evidence.
6. additional commands only where early evidence supports them.

### Evidence boundary

The original PDP-7 B source and exact first diskless PDP-11 `dc` source are not known to survive. The result will therefore be class B, not restored original code.

Later V1/V2 behavior may be used as comparative evidence but must not be silently backported.

### Gate

The reconstructed program fits and runs on the historically configured diskless PDP-11, using the complete PDP-7 development path, with a documented feature/provenance matrix.

### Fallback

Stop at the strongest defensible calculator that the evidence and reconstructed environment support. A smaller honest reconstruction is preferable to a feature-complete historical fiction.

---

## Final deliverables

The project should ultimately produce more than a working emulator session:

- reproducible PDP-7 and PDP-11 SIMH configurations;
- source for all reconstruction code;
- automated modern verification tests;
- provenance/claim documentation;
- generated paper-tape artifacts with reproducible build instructions;
- a short technical write-up of what is known, reconstructed, substituted, and still unknown;
- an end-to-end demonstration script or documented session reproducing the PDP-7 -> paper tape -> diskless PDP-11 workflow.
