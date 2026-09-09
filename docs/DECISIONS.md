# Decision Log

Short append-only project decisions. Reverse a decision by adding a new entry rather than rewriting history.

## D0001 — Historical honesty over exact-looking simulation

**Status:** accepted

The project is an exercise in using surviving parts in a way that fits historical accounts, while clearly stating what is original, reconstructed, substituted, or unknown. We will not claim exact recovery where source has been lost.

## D0002 — Produce a reusable public project, not only an emulator session

**Status:** accepted

The repository, documentation, tests, generated artifacts, and reproducible workflow are first-class deliverables. Chat instructions alone are not considered project output.

## D0003 — Dependency-gated implementation

**Status:** accepted

Do not begin later stages merely because the next emulator command is available. Each roadmap stage has an explicit gate intended to expose architectural failures early.

## D0004 — Modern tooling is allowed as instrumentation

**Status:** accepted

Modern host-side tests, scripts, converters, CI, and verification tools are encouraged during reconstruction. They must be class M and excluded from the final historical code-generation path unless explicitly documented.

## D0005 — No silent optional PDP-11 hardware

**Status:** accepted

The diskless PDP-11/20 remains configured without KE11 unless historical evidence justifies enabling it. Missing arithmetic operations should initially be handled in software or by restricting the supported B subset.

## D0006 — Bell Labs paper-tape encoding remains unresolved

**Status:** accepted

Paper-tape transfer is historically attested, but the exact Bell Labs record/loading format is not yet established. A contemporary DEC format may be used as class C if required, but must not be described as the Bell Labs format without evidence.

## D0007 — Repository-wide licensing deferred

**Status:** accepted

Do not add a blanket repository license until we decide how newly written code, documentation, imported PDP-7 material, reconstructed B material, and generated artifacts will be separated. Imported source must retain upstream licensing/provenance.

## D0008 — Split the threaded-B runtime gate into Stage 3A and Stage 3B

**Status:** accepted

Stage 3A is limited to the strongly evidenced R3/R4/R5 direct-threaded nucleus
and documented `c`, `x`, `va`, `b12`, and `b1` semantics. The reconstruction
is class B because Thompson's detailed manual is from January 1972 and the
exact late-1970 source is lost. Control flow, calls, returns, real frame setup,
arguments, and the remaining minimal execution machinery are a separate Stage
3B gate; Stage 3A success must not be described as completion of all Stage 3.

## D0009 — Stage 3B pending-frame and return-value convention

**Status:** accepted

Reconstructed argument-bearing calls follow the observed Stage 1 ordering:
function value, mark, left-to-right arguments, call. `mark` reserves
`[old R4, callee]` at R5 and records the pending frame in temporary R2 without
changing R4; `call` replaces the callee word with saved R3 and activates R4.
Arguments occupy frame words 2 onward. Value return replaces saved-R3 word 1
with the result and leaves R5 at word 2; void `n11` leaves R5 at word 1. This
is class B inference consistent with class-A frame semantics, Stage 1 output,
and B/C archaeology, not recovered late-1970 source.

## D0010 — Persistent project PDP-7 and development identity

**Status:** accepted

`machines/pdp7` is the authoritative persistent working host; `../PDP-7` is a
read-only pre-transition reference. Project work normally uses `shankao` and
does not change historical accounts or hard-linked authentic files merely to
bypass permissions. Working copies and generated artifacts remain
distinguishable from authentic, reconstructed, and restored originals.

## D0011 — Separate assembler, compiler, and tape transport

**Status:** accepted

Stage 4 reconstructs `as11`, a B-written PDP-11 assembler running on the
PDP-7. Stage 5 separately reconstructs `b11`, which emits a readable PDP-11
threaded assembly/representation for `as11`. Paper-tape construction and
loading are Stage 7 transport concerns and belong to neither tool. This lets
Stage 6 verify compiler and assembler with class-M loading before introducing
the historically uncertain tape boundary.

## D0012 — Contemporary DEC loader only as a labelled fallback

**Status:** accepted

Physical PDP-7-to-PDP-11 paper-tape transfer is attested, but its exact Bell
Labs format remains unknown. DEC Absolute Binary/Absolute Loader machinery
may be selected later as class C if no stronger evidence emerges. Selection
would establish a contemporary substitute, not evidence that Bell Labs used
that convention.

## D0013 — Repository endpoint is the December 1970 disk transition

**Status:** accepted

The required completion gate is a reproducible first disk-backed PDP-11 UNIX
environment consistent with surviving evidence for the December 1970 disk
arrival. Core-only/RAM-filesystem UNIX and disk migration are explicit
high-risk stages. Later 1971 development toward First Edition is outside this
repository's required scope and may be continued separately.

## D0014 — Split `as11` reconstruction into five dependency gates

**Status:** accepted

Stage 4 proceeds as: 4A PDP-7 B input-restart/text-output substrate; 4B
language and two-pass symbol engine without target encoding; 4C independently
verified KA11 encoding; 4D integrated usable two-pass `as11`; and 4E the Stage
3 nested-call gold round trip. Parent Stage 4 completes only after all five
pass. This split isolates historical B I/O, language inference, encoding,
resource limits, and target execution rather than debugging them together.

## D0015 — Normal PDP-7 development uses the evolving persistent host

**Status:** accepted

Normal project development and tests run directly on `machines/pdp7` as
`shankao`; its filesystem is expected to evolve. Git supplies recovery, an
uncommitted dirty image is acceptable during active work, and each successfully
completed PDP-7 development substage normally commits an image checkpoint with
useful native artifacts retained. Legitimate changes are not reverted to
preserve an old hash. Disposable image copies are reserved for experiments with
a specific destructive or high-risk reason, not routine runner architecture.

## D0016 — Preserve native computation despite PDP-7 execution cost

**Status:** accepted

Native text transfer where required, B compilation, assembly/linking, program
execution, and filesystem operations remain on the PDP-7 even when slow. Class-M
tools may supervise and optimize orchestration but must not replace historical
computation solely for convenience. Discovery uses a persistent interactive
SIMH session; automation follows a demonstrated native procedure.

## D0017 — Stage 4B compact semantic front end

**Status:** accepted

The reconstructed `as11` front end uses six-word, eight-significant-character
global entries (64 capacity), a separate two-word occurrence/address table for
numeric `0:`–`9:` labels (64 definitions), and a PDP-11 byte-address location
counter. Assignments require immediate resolution; only fixed-size bare words
may forward-reference labels. Expressions are octal with unary/binary `+`/`-`
and square-bracket grouping. Stage 4B emits semantic traces only. Instruction
and addressing encoding remain a separate Stage 4C concern.

## D0018 — Preserve selected PDP-7 development states as physical snapshots

**Status:** accepted

Every passing PDP-7 development gate continues to checkpoint the authoritative
`machines/pdp7` image. In addition, a state that meaningfully exposes a distinct
point in the development journey may be materialized as an exact ordinary Git
file under `eras/`, with source commit, original path, and SHA-256 recorded.
Snapshots are mutable version-controlled files, not an era format: no manager,
boot wrapper, immutability layer, or copy-on-boot mechanism is required. The
proper representation of later PDP-11 RAM, tape, disk, and paired-machine eras
is deferred until operational experience supplies real requirements.

For PDP-7-only eras, the established self-contained form is `README.md`, the
recovered `boot.rim`, `pdp7.fs`, and an era-local `pdp7.simh` that attaches that
filesystem. The tiny bootstrap/configuration duplication is deliberate; no
wrapper or management abstraction is introduced. This form is not presumed to
fit later multi-machine eras.

Starting with the next passing PDP-7 development checkpoint (Stage 4C), the
native `dd/shankao/readme` should concisely state what works and what remains
absent. It evolves during normal native work and naturally enters later
snapshots; exact older checkpoint images are never edited retroactively to add
it.

## D0019 — PDP-7 cross-tools are bootstrap scaffolding

**Status:** accepted

The reconstructed PDP-7 `as11` and `b11` exist to reach useful destination
PDP-11 capabilities and the attested cross-development path. Their scope follows
bootstrap sufficiency: implement evidenced features needed by the next gate,
not a permanent comprehensive PDP-11 development environment on the PDP-7.
Later migration toward native PDP-11 development is part of the intended
historical arc, while the PDP-7 remains preserved as fallback and history.

## D0020 — Stage 4C high-memory symbol arena is provisional

**Status:** superseded for gate interpretation by D0021; allocator remains provisional

The encoder made Stage-4B's static tables incompatible with ordinary B.
Current Stage 4C retains the measured 48-global/10-local demand, uses five
words per global by storing state in unused high bits of the first packed
ASCII name word, and places records below `bl.s`'s two 64-word I/O buffers.
This is native B symbol processing, not host substitution. Encoding succeeds,
but maximum occupancy leaves only five B-stack words and fails the substantial
regression, so this layout is evidence and a candidate—not a completed ABI.

Follow-up native characterization found exact traces at 38 globals/10 numeric
locals, while 39 globals fails with even one local; a Stage-3-shaped 17/5
workload passes with a 105-word larger static separation. The capacity issue is
therefore localized, but no lower limit or guard is accepted yet. The leading
candidate is a zero-growth 38-global allocation guard using the existing `gf`
error. This remains an unimplemented investigation result, not a final limit.

## D0021 — Stage 4B, 4C, and 4D own distinct capacity questions

**Status:** accepted

Stage 4B guarantees language/parser/symbol semantics and records the capacity
of its standalone implementation. Stage 4C guarantees preservation of those
semantics, KA11 encoding correctness, and feasibility of the current realistic
Stage-3-shaped bootstrap workload. Stage 4D owns the final textual map and the
complete assembler's measured bootstrap capacity, clean native exhaustion
behavior, and safety margin.

Accordingly, Stage 4B's genuine 48-global/10-local result remains historical
evidence but is not a permanent minimum for every larger intermediate build.
Stage 4C closes with the measured frontier fully visible and without adopting
the proposed 38-global guard. Symbol count alone is not a sufficient safety
model: 39 globals/0 locals passed while 39 globals/1 or more failed. Final
capacity decisions wait for Stage 4D's actual integrated architecture.

## D0022 — The PDP-7 UNIX migration corpus defines the destination workload

**Status:** accepted

The surviving/restored PDP-7 UNIX system is the principal source base for the
late-1970 PDP-11 UNIX migration. `as11`, threaded B, `b11`, tape transport,
and `dc` remain essential bootstrap scaffolding, not the definition of the
destination system. Bootstrap and UNIX-migration tracks may advance in
parallel where dependencies allow and converge on the PDP-11. Once useful
development can move to the PDP-11, capability should ratchet in that
direction rather than expanding the PDP-7 into a permanent comprehensive
cross-development environment.

Before Stage 4D adds features, a planning gate will audit the selected local
PDP-7 kernel/command corpus, its provenance, responsibilities, intended target
semantics, omissions, and derived assembler requirements. Stage 4C's
Stage-3-derived inventory remains a verified encoder nucleus and regression
corpus, not the final `as11` specification. This reframing preserves all
completed stage results and labels.

## D0023 — Refine PDP-7 source provenance without replacing A/B/C/D/M

**Status:** accepted

Migration work uses the namespaced tags `P7-A-I` and `P7-A-II` for the two
contemporary listing/source lineages, `P7-R` for restored or modified working
derivatives, `P7-C` for required reconstruction/repair, and `P7-O` for other
PDP-7 material whose origin must be stated separately. These refine, but do
not replace, the repository-wide provenance classes. In particular, a file's
presence in the restored source tree does not prove it is an untouched
contemporary original. Detailed assignments wait for the migration-corpus
audit.

## D0024 — Future work uses named, converging milestones

**Status:** accepted; supersedes prospective Stage 4D–12 numbering, not
completed Stage 0–4C labels

Completed Stage 0, 1, 2, 3, 4A, 4B, and 4C labels remain stable historical
identifiers. Prospective work is organized as named gates and workstreams so
numbering cannot imply that the bootstrap/B path must finish before UNIX
migration begins. Earlier decisions that mention prospective Stage 4D–12
numbers retain their historical meaning, but their dependencies and current
names are governed by `PLAN.md`.

The bootstrap track contains Unix-driven `as11` completion, the Stage-3 gold
round trip, `b11`, modern-load integration, paper-tape transport, “Across the
Floor,” calculator work, and `dc0`. The migration track contains corpus
definition, the bare KA11 substrate, core-only PDP-11 UNIX, and the RF11/RS11
transition. Neither `b11`, the calculator, nor `dc0` is a prerequisite for
core-only UNIX unless a later workload-specific dependency proves otherwise.
Both tracks consume the provenance-audited migration corpus where relevant
and converge on useful PDP-11 capability.

## D0025 — Freeze provisional PDP-7 migration corpus v1

**Status:** accepted; supersedes D0023's provisional `P7-*` tag names

Immediate machine-contract and later cross-assembler requirements derive from
the responsibility-level corpus frozen in `UNIX-MIGRATION.md`: selected
responsibilities from A1-derived `s1.s`–`s8.s`, with `s9.s` deferred, plus
`cat` from A1 and `ls`, `rm`, `sh`, and `stat` from A2, all through their
restored B forms and any narrow local C interpretation. A1/A2/B/C/D are
layered source-lineage categories under the repository-wide A/B/C/D/M
confidence policy. The freeze is provisional workload control, not proof of
the exact December-1970 source set.

The core-only process interface follows the strongest surviving PDP-7 model:
`fork`, manual child-image replacement, minimum `smes`-like foreground
synchronization, and `exit`. Modern `exec`, `wait`, and full pathname
semantics are not assumed for the pre-disk interval; their introduction is an
RF11-transition research question. A two-process shell/child model and a
single-directory RAM-backed filesystem are acceptable conservative first
milestones, not claims about the lost kernel's exact limits.

The next gate is research/design of the bare KA11 machine-layer contract.
Future instructions and assembler features listed by the corpus are
requirements candidates only; no encoder or target implementation is changed
by this decision.

## D0026 — Freeze the bare KA11 machine-layer research contract

**Status:** accepted

The PDP-11/20 KA11 has no hardware user/kernel protection modes, separate
user/kernel register banks, or automatic kernel-stack switch. System and user
code share one physical address space under software convention. TRAP saves
PC/PS through the current R6 stack and vectors through 034/036; it transfers
control without a privilege-mode transition. Software process state therefore
conceptually preserves R0–R5, SP, PC, and PS.

The initial core-only scope uses vectors 004, 034, 060, and 064; targets an
interrupt-driven KL11 at `177560`–`177566` and BR4; and does not require a
periodic scheduler. Polling is diagnostic scaffolding only. RAM-backed
filesystem blocks and process images use replaceable abstractions so RF11 can
later replace the backend without rewriting their higher-level semantics.

Installed RAM is `000000`–`057777`, but the approximate historical 12 KB
system envelope does not freeze exact system, user, stack, or storage
boundaries. No RAM block/inode geometry or process-swap partition is selected.
The later V1 16 KB / 8 KB layout is descendant evidence only. The next gate
must derive the active-user size and complete execution/RAM layout from the
provisional command workload before implementation.

## D0027 — Freeze provisional core-only execution/memory contract v1

**Status:** accepted as a conservative reconstruction; implementation not
started

The historically attested 24 KB target and approximate 12 KB OS/tiny-user/
remaining-RAM-storage account constrain, but do not recover, the exact memory
layout. Version 1 selects byte boundaries `SYS_LIMIT=030000`,
`USR_BASE=030000`, `USR_TOP=040000`, and `RAM_BASE=040000` through
`RAM_TOP=060000`: a 12 KB system envelope, 4 KB fixed user window, and 8 KB
shared RAM arena. `USR_STATIC_LIMIT=036000` is only a soft 3 KB image/1 KB
stack-and-staging budget. Actual kernel, command, stack, and argument sizes
remain empirical gates.

Pre-disk commands are raw absolute images loaded and entered at `030000` by a
shell-controlled high-memory stub. They have no `a.out` header, relocation,
target symbols, or kernel `exec`. The command argument frame uses the later
natural argc/argv/NUL-byte-string convention as descendant-constrained
reconstruction, not recovered pre-disk behavior.

The syscall ABI retains PDP-7-shaped symbolic `sys name`, inline argument
words, R0 accumulator/result semantics, and R0=`-1` errors over the KA11 TRAP
mechanism. Exact call numbers remain unfrozen; the later carry-error convention
is not adopted. PDP-7 source establishes child-first `fork` with two return
continuations and supports a cooperative, single-resident shell/child model
with minimal `smes`, without a clock scheduler.

Process backing compactly saves the lower live image and upper live stack,
not the empty gap. First Edition stack packing is compatibility evidence only.
The shared RAM arena provisionally has sixteen 512-byte blocks, with eight
direct blocks limiting RAM-only files to 4096 bytes and no fixed filesystem/
process partition. Block size is descendant-constrained reconstruction, not
an attested RAM-disk geometry.

The filesystem/data-structure follow-on described here is now complete in
provisional contract v1; D0028 records its result.

## D0028 — Freeze provisional core-only filesystem/data contract v1

**Status:** accepted as a conservative reconstruction; implementation not
started

The selected system preserves PDP-7 predecessor semantics that fit its
cooperative scope: ten lowest-free, three-word descriptors copied per process;
one current inode buffer rather than an inode cache; negative link counts; and
a compact twelve-word inode plus inode-number `status` result. It deliberately
has no global open-file table or shared open-file-description semantics.

The PDP-11 inode remains twelve words but substitutes an eighth direct
512-byte block pointer for the unused selected-path unique-number mechanism;
uid, negative links, byte size, and relevant permission/type flags remain.
The one directory uses 10-byte entries (16-bit inode and eight-byte NUL-padded
name). First Edition independently corroborates that natural directory shape,
but its richer 32-byte inode, timestamps, positive link counts, and 34-byte
`stat` are descendant evidence and are not imported.

RAM block 0 holds sixteen 24-byte inode slots, block 1 holds the fixed root,
and blocks 2–15 form a common allocation arena for direct file data and compact
process backing. Separate 16-bit block and inode maps, one 512-byte block
buffer, two provisional 64-word process records, and separate tty input/output
special-inode semantics complete v1. Direct files stop at 4096 bytes; there is
no indirection, chained disk free list, inode cache, generalized device layer,
or pathname hierarchy.

The initial filesystem plus worst-case shell backing and writable-test
headroom must fit the sixteen-block arena. Exact initial inode assignments,
whether `sh` occupies a file, structure offsets, tty ring capacity, translated
sizes, and filesystem/process allocation pressure remain empirical. RF11
should preserve high-level algorithms and block I/O, but persistent metadata
may evolve; it is not constrained to a zero-metadata-change backend swap.

At acceptance, the next gate was a repository-aware planning pass for the
first implementation slice. D0029 records its completed integration result.

## D0029 — Close native-as11 Stage-3 gold transport and streamline development host

**Status:** accepted and demonstrated

The active PDP-7 development configuration runs unthrottled, while every
preserved era config retains `set throttle 400K`; the established 80 ms
terminal-transfer pacing is unchanged. The older `pdp7-unix-copy` import was
audited as an unused subset with no unique tracked project paths and removed,
with its provenance retained in Git and the immutable import manifest.

Stage-3B test L is now readable `as11` input assembled natively on the PDP-7.
Class-M transport accepts only deterministic `i`/`x`/`w` records, rejects
malformed or duplicate addresses, verifies instruction records with the
independent Stage-2-backed Stage-3 manifest, and deposits the exact native
map without encoding or substitution. The PDP-11/20 prints `D`. This closes
the gold integration proof but does not make Stage 4C a target-complete
assembler. At that checkpoint the next bounded slice was KL11 polling I/O;
D0030 records its completion and advances to low-core vectors/RTI.

## D0030 — Prove KL11 polling before interrupt machinery

**Status:** accepted and demonstrated

A modern readable diagnostic uses only the existing Stage-4C instruction
surface to poll receiver DONE and transmitter READY, read/write their data
buffers, save two input bytes, and halt. Native PDP-7 `as11` produced all 33
executed words; class-M code only parsed, oracle-checked, and deposited them.
With PTY echo disabled, controlled `A` and `B` inputs produced `AB`, and RAM
retained both bytes. No receiver/transmitter interrupt enable or vector was
used. The next gate is low-core vector entry and RTI return, followed by
interrupt-driven KL11 console.

## D0031 — Canonicalize active configs and preserve cross-developed PDP-11 execution

**Status:** accepted and demonstrated

Active tools use `machines/pdp7/pdp7.simh` for the unthrottled authoritative
PDP-7 development host and `machines/pdp11/pdp11.simh` for a clean 24 KB KA11
baseline. The PDP-11 config deposits or runs no program and does not configure
paper tape, storage, KE11, or the line clock. This SIMH build exposes CLK as
inherent and refuses disabling it, so current diagnostics simply leave it
untouched. The obsolete reconstructed volatile bootstrap config is retained by
Git history, not as a duplicate active file.

The first operationally justified PDP-11 era is `eras/pdp11-crossdev`: an
era-local copy of the clean config plus the native-PDP-7-assembled KL11 polling
deposit script. It preserves a cross-development execution state, not a
self-hosted PDP-11, UNIX system, or precedent for later RAM/tape/disk era
layouts. Existing PDP-7 era contents remain unchanged.
