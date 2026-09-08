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
