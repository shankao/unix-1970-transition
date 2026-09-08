# PDP-7 to PDP-11 UNIX migration

## Provisional corpus freeze v1

This is the first source-level freeze of the PDP-7 to PDP-11 migration
workload. “Frozen” means that immediate PDP-11 UNIX design and further
cross-assembler requirements are derived from this corpus until evidence or
implementation findings justify a recorded revision. It does **not** mean
that this is the historically proven, exact December-1970 source set.

The destination is defined by selected late-1970 PDP-7 UNIX responsibilities,
not by how much of `as11` or `b11` can be built. The surviving/restored PDP-7
system is the principal source base. Cross-development tools, threaded B, and
standalone B programs are bootstrap scaffolding rather than the PDP-11 UNIX
specification. Exact 1970 PDP-11 kernel and command sources are not known to
survive; the target is a conservative reconstruction, not First Edition UNIX.

## Evidence and provenance layers

Repository-wide A/B/C/D/M confidence labels remain authoritative. For this
migration audit, the following layered source-lineage categories refine them:

- **A1** — contemporary listing in the Norman Wilson / companion-binder scan
  corpus, probably the hypothetical “Unix Book I” lineage;
- **A2** — contemporary listing in Dennis Ritchie's identified “Unix Book
  II” corpus;
- **B** — working restored or modified source derived from an A1/A2 listing;
- **C** — local repair, reconstruction, or interpretation where contemporary
  material is broken, ambiguous, annotated, incomplete, or insufficient
  as-is;
- **D** — other PDP-7 material not directly derived from a surviving
  contemporary listing.

These source layers may overlap hierarchically: a routine may have A1
ancestry, an A1-derived working B form, and a narrow C correction. A local
repair does not make the entire file reconstruction, and a runnable restored
file is not thereby an untouched contemporary source. In project-wide usage,
A1/A2 are authentic evidence; source-layer B/C must still receive the
appropriate project-wide reconstruction/restoration classification in the
specific claim. Source-layer D is an origin category, not a confidence grade.

The earlier provisional `P7-A-I`/`P7-A-II`/`P7-R`/`P7-C`/`P7-O` names are
superseded by this audit vocabulary. No detailed scan-to-source line audit is
claimed here beyond the source-level ancestry recorded below.

The checked-in audit basis is the paired material under
`machines/pdp7/pdp7-unix/scans/`, `src/sys/`, and `src/cmd/`: contemporary
transcriptions/listings for `s1.s`–`s9.s` and the five commands, alongside the
working restored forms. The formerly imported parallel `pdp7-unix-copy` tree
was an older redundant subset, not an independent provenance source; its
original import remains recorded in Git and the import manifest, while the
active tree is the sole working copy.

## Two cooperating tracks

```text
Ritchie-oriented bootstrap                 Thompson-oriented UNIX migration
as11 -> threaded B -> b11 -> dc            PDP-7 kernel/commands -> PDP-11
                    \                       /
                     useful PDP-11 system
```

These labels describe responsibilities, not exclusive authorship claims. The
tracks may proceed independently where their real dependencies allow. In
particular, `b11`, the calculator, and `dc0` are not prerequisites for the
core-only UNIX milestone unless a selected workload later proves otherwise.
Once useful development can run on the PDP-11, capability should ratchet
toward it rather than making the PDP-7 a permanent comprehensive toolchain.

## Kernel responsibility corpus

All `s1.s` through `s8.s` have strong contemporary A1 listing ancestry and
working source-layer B derivatives. Whole files are not migration units: the
selected responsibilities below are. Machine-specific PDP-7 mechanisms
constrain semantics but are not translated literally.

### `s1.s` — A1 -> B

Retain as evidence for syscall entry/dispatch responsibility, saved
user/process state, process selection and backing-store interaction, and
syscall return. Do not mechanically translate PDP-7 CAL entry,
AC/MQ/auto-index save conventions, PDP-7 interrupt machinery, or RB disk
operations. PDP-11 traps, vectors, registers, and processor-stack handling are
new machine-specific reconstruction.

### `s2.s` — A1 -> B

Initial syscall responsibilities: `status`, `open`, `creat`, `close`, `read`,
`write`, and `unlink`.

Initially defer seek/tell, link, rename, chmod/chown, uid operations, time,
`capt`/`rele`, and calls not demanded by the first corpus.

### `s3.s` — A1 -> B

Select process lookup/table responsibilities, `fork`, `exit`, the minimum
`smes`/wake-up behavior required by the shell, and special-file/tty dispatch
concepts. General message IPC is not initially required.

### `s4.s` — A1 -> B, with possible local C interpretation

Select allocation/freeing semantics, copy/zero helpers, and character-queue
responsibility if needed by the tty implementation. Do not translate
RB-specific caching, PDP-7 self-modifying tricks, or the exact interrupt-safe
queue implementation merely because they survive.

### `s5.s` — A1 -> B

Select process backing-store responsibility; file/fnode assignment and
get/put responsibilities; required access checks; required sleep/wakeup
concepts; `dslot`; and `icreat`. PDP-7 disk swap is evidence for the
abstraction, while the core-only PDP-11 will use RAM backing. PDP-7
packed-character machinery need not survive where PDP-11 bytes replace it
naturally.

### `s6.s` — A1 -> B

This is the principal filesystem-algorithm source. Select `itrunc`, name
lookup, inode acquire/release, directory get/put, block mapping/allocation
interaction, and inode read/write. Large/indirect-file support remains
conditional until RAM-filesystem requirements establish a need before RF11.

### `s7.s` — A1 -> B

Use as semantic evidence for console input/output completion, blocked-process
wakeup, and character queues. PDP-7 device instructions are not translated
literally; the KL11 layer is new machine-specific code.

### `s8.s` — A1 -> B

Use as structural evidence for process state, per-process file state,
current-directory state if needed, in-core inode and directory representation,
filesystem globals, character queues, and cold-start responsibilities. Do not
preserve PDP-7 offsets or 18-bit layouts. Core-only cold start initializes
RAM-backed storage and enters the shell environment rather than literally
reproducing disk-oriented PDP-7 startup.

### `s9.s` — deferred

Installation, filesystem creation, and persistent-media work belong with the
RF11 transition. `s9.s` does not drive the core-only system.

## Initial command corpus

| Command | Source layer | Initial role |
| --- | --- | --- |
| `cat` | A1 -> B | strong semantic migration candidate |
| `ls` | A2 -> B | minimal namespace inspection |
| `rm` | A2 -> B | near-semantic transliteration candidate |
| `sh` | A2 -> B | command loading and parent/child control |
| `stat` | A2 -> B | second-tier metadata validation |

Contemporary listing evidence exists for all five, while runnable forms may
contain restoration changes.

### `sh`

Retain command input, simple parsing, `fork`, manual loading/replacement of
the child image, I/O redirection, and foreground parent/child synchronization.
Background `&`, system-directory search/link tricks, login/logout integration,
and other conveniences may be deferred if unnecessary.

### `cat`, `rm`, `ls`, and `stat`

`cat` exercises `open`, `read`, `write`, and `close`; replace PDP-7 packed
characters naturally with PDP-11 byte handling. `rm` iterates arguments,
calls `unlink`, and reports failure. The first `ls` may read the directory
sequentially and print names without sorting or long format; that is a
resource adaptation, not a claim about lost PDP-11 behavior. `stat` validates
metadata/status but need not block the earliest shell prompt.

## Core-only process and syscall contract

Do not introduce modern `exec` and `wait` merely because later PDP-11 UNIX has
them. The strongest surviving PDP-7 model is:

```text
fork
    -> child manually loads/replaces its image
    -> parent synchronizes through minimum smes-like semantics
    -> child exits
```

Ritchie's retrospective associates modern `exec`, modern `wait`, and full
pathnames with the first completed PDP-11 system after disk arrival, but does
not establish their exact point of introduction during the pre-disk interval.
The provisional chronology is therefore PDP-7-shaped
fork/exit/manual-load/`smes` for core-only operation, followed by focused
investigation of `exec`, `wait`, and full pathnames during RF11 convergence.
This is conservative reconstruction from predecessor and later historical
evidence, not recovered 1970 PDP-11 source.

The provisional core-only syscall surface is:

```text
fork  exit  smes
open  creat close read write unlink status
```

Only synchronization needed by the foreground shell is required from `smes`.
Console I/O uses ordinary `read`/`write` special-file semantics. Initially
deferred are `exec`, `wait`, `rmes`, link, rename, seek, tell, `chdir`, chmod,
chown, setuid/getuid, time, and any other call not demanded by this corpus.
Actual migration may promote an operation if it proves indispensable.

A conservative first process model may keep a resident shell, preserve its
image/state in RAM backing at `fork`, run a manually loaded child in the user
area, and restore/wake the shell when the child exits. A two-process
parent/child model may suffice. This is a simplification, not an assertion
that the lost system had exactly two process slots. Clock preemption, fair
scheduling, useful background execution, and multiple interactive terminals
are not initial requirements.

## Core-only filesystem contract

The minimum RAM-backed filesystem provides:

- inode/file identity and directory entries;
- ordinary files and a console special file;
- per-process descriptor and per-open offset state;
- open/create/read/write/close, unlink, and status;
- allocation and freeing of RAM-backed blocks.

A single-directory namespace is acceptable for the first milestone. Full
pathnames and `chdir` are not prerequisites. The completed follow-on contracts
now provisionally freeze 512-byte RAM blocks and the small structures described
in `PDP11-FILESYSTEM-CONTRACT.md`; these are reconstruction, not recovered
geometry.

## Workload-derived `as11` requirements

Stage 4C remains the validated B-bootstrap encoder nucleus:

```text
add asl asr bne bpl br clr cmp halt jmp mov movb tst tstb
```

Its implementation is unchanged. The provisional migration corpus clearly
justifies this instruction requirement set:

```text
jsr rts inc dec sub beq bmi bit bic bis cmpb clrb rti
```

`jsr` and `rts` are already implemented Stage 4C control-class extensions;
the remaining entries are future requirements, not current encoder claims.

The KA11 TRAP family is required for a system-call mechanism, likely exposed
eventually through a `sys`-style pseudo-operation after the ABI is settled.
Likely but not yet demonstrated by translated source are signed-comparison
branches, unsigned/carry branches, `com`, `neg`, byte forms such as
`bitb`/`bicb`/`bisb`/`incb`/`decb`, `wait`, and `reset`. An item moves from
likely to required only when actual translated workload or a settled machine
contract demonstrates the need.

Do not leak descendant-machine facilities into the KA11 target. `sob`, `sxt`,
and later multiply/divide/shift machinery are examples that must not be
assumed available.

The corpus also justifies assembler-language support for:

- origin/location-counter control and symbol/equate assignment;
- raw word and raw byte emission;
- reserved byte/word storage and even-address alignment;
- character constants and sufficient string/data literals;
- unary bitwise complement for natural KA11/BIC mask expressions;
- eventually a `sys`-style pseudo-op after the syscall ABI is settled.

Location-counter/origin control, assignment, and raw-word emission already
exist in the Stage 4B/4C language. Raw bytes, reservation, alignment,
characters/strings, unary complement, and `sys` remain future requirements.
The current expression engine has unary minus and binary `+`/`-`, but no
equivalent complement operation. This finding does not implement one.

Macros, conditional assembly, convenience includes, relocatable objects,
external-symbol records, a linker, libraries, and elaborate sections remain
out of scope unless a real workload establishes a need. The intended cross
assembler remains a small whole-program bootstrap tool. None of the future
instructions or language features listed here has been implemented by this
audit.

## Core-only success criterion

A conceptual validation sequence is:

```text
boot or deposit core-only PDP-11 UNIX
    -> initialize machine, console, and RAM storage
    -> enter sh
    -> ls
    -> cat existing-file
    -> ls >newfile
    -> cat newfile
    -> stat newfile
    -> rm newfile
    -> ls
```

Fixture names and output are not historical claims. The sequence proves
syscall entry/return, process creation/restoration, command loading, console
and special-file I/O, namespace operation, create/read/write/close,
metadata/status, unlink, and shell redirection.

## RF11-era deferrals

The following remain outside the core-only freeze pending the RF11 research
gate:

- real RF11/RS11 block devices and persistent disk filesystem;
- disk-backed process swapping;
- exact introduction of modern `exec` and `wait`;
- full pathname traversal;
- normal `init`/login environment and a larger completed-system user area;
- additional terminal conveniences;
- disk recovery, installation, and filesystem-creation machinery.

First Edition source is descendant evidence, not the specification for these
items.

## Completed machine, execution, and filesystem research

The bare KA11 research result is authoritative in
[`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md). It fixes hardware
facts—most importantly the absence of hardware user/kernel modes, current-stack
TRAP behavior, and KL11 interfaces. That hardware gate left exact user/RAM
boundaries and storage geometry unfrozen; the reconstruction contracts below
now select provisional values.

The provisional execution/memory contract v1 is authoritative in
[`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md). It freezes a
conservative 12/4/8 KB system/user/RAM layout, raw absolute command images,
shell-controlled replacement, PDP-7-shaped syscall semantics, child-first
cooperative execution, compact process backing, and a provisional 512-byte
RAM-block geometry. These are reconstruction choices constrained by the
evidence, not recovered pre-disk source.

The provisional filesystem/data-structure contract v1 is authoritative in
[`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md). It freezes
small predecessor-derived structures and capacity invariants without importing
First Edition's richer persistent filesystem. High-level algorithms and the
block-I/O boundary should survive RF11 arrival, but persistent metadata may
legitimately evolve; RF11 is not promised to be a metadata-free backend swap.

The next gate inspects current repository implementation reality and produces
a bounded first-slice plan. It does not authorize implementation automatically.
