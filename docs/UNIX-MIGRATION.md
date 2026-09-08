# PDP-7 to PDP-11 UNIX migration plan

## Purpose

The destination is not defined by how much of `as11` or `b11` can be built.
It is defined by the late-1970 PDP-7 UNIX responsibilities that must be moved
to the diskless PDP-11/20. The surviving/restored PDP-7 system is therefore
the principal source base for the UNIX migration. Cross-development tools,
the threaded-B runtime, and standalone B programs are essential bootstrap
scaffolding, but they are not the PDP-11 UNIX specification.

This document is a planning boundary, not a completed source audit or an
authorization to port anything. Exact 1970 PDP-11 kernel and command sources
are not known to survive. The result will be a conservative reconstruction,
not First Edition UNIX.

## Two cooperating tracks

The historical work is usefully modeled as two parallel tracks:

```text
Ritchie-oriented bootstrap                 Thompson-oriented UNIX migration
as11 -> threaded B -> b11 -> dc            PDP-7 kernel/commands -> PDP-11
                    \                       /
                     useful PDP-11 system
```

The labels describe responsibilities, not exclusive authorship claims. The
tracks can advance independently where their dependencies allow and converge
on the PDP-11. Once useful development can run there, capability should
ratchet toward the PDP-11 rather than turning the PDP-7 cross environment into
a permanent, comprehensive toolchain.

## Provisional first migration corpus

The first corpus to audit is derived primarily from the local PDP-7 UNIX
sources:

- kernel/system responsibilities in `s1`, `s2`, and `s3`;
- selected responsibilities from `s4`, `s5`, and `s6`;
- console-relevant parts of `s7`;
- structures, constants, and cold-start material from `s8` as required;
- an initial command set of `sh`, `cat`, `ls`, `rm`, and `stat`.

These names are selection candidates, not a statement that every line should
be transliterated or that their current restored files share one provenance.
Before implementation, the corpus-definition gate must inventory the actual
local files and variants, identify each selected responsibility, record its
provenance and intended PDP-11 semantics, state omissions, and derive the
PDP-11 instruction/directive requirements it introduces.

The first destination milestone is a single-console PDP-11/20 test system
with a RAM-backed filesystem or storage area, a small active user area,
process creation and program execution, basic file I/O, and a tiny interactive
shell environment. A 24 KB machine, a pre-disk system, and a rough division
among operating system, small user area, and RAM-backed storage are
historically attested in retrospective accounts. The exact late-1970 memory
partition and implementation are unknown and remain reconstruction choices.

## PDP-7 source provenance tags

The repository-wide A/B/C/D/M labels remain authoritative. Migration work may
refine PDP-7 source provenance with these namespaced tags:

- **P7-A-I** — contemporary PDP-7 material in the original surviving
  listing/source (“Book I”) lineage;
- **P7-A-II** — contemporary PDP-7 material in the later-discovered Ritchie
  “Unix Book II” corpus;
- **P7-R** — working restored or modified source derived from contemporary
  listings; authentic ancestry does not make the working file untouched;
- **P7-C** — reconstruction or repair needed where surviving material is
  incomplete, ambiguous, or insufficient to run;
- **P7-O** — other PDP-7 material not directly tied to those listing corpora;
  its origin must be recorded separately.

`P7-A-I` and `P7-A-II` refine class A. `P7-R` records transformation history
and must be classified A/B at the claim or code level as appropriate. `P7-C`
is normally class B. `P7-O` is deliberately not a confidence claim. These
names avoid overloading the established repository-wide B and C labels.

No blanket tag is assigned here to all files under restored `src/sys` or
`src/cmd`. That requires a file-by-file local provenance audit before a
migration component is selected.

## Workload-driven assembler growth

Stage 4C's mnemonic inventory came from the proven threaded-B runtime. It is a
validated KA11 encoder nucleus and B-bootstrap test corpus, not the final
historically derived `as11` requirement. Future growth follows:

```text
select a migration responsibility
    -> establish source provenance and target semantics
    -> translate it conservatively
    -> identify a missing instruction or directive
    -> extend as11 only when that requirement is real
```

The Stage 4C capacity frontier remains valid evidence. Its practical impact
must be measured against the selected migration workload and the final Stage
4D output path; it is not resolved by this planning document.

## Destination layers

After the corpus-definition gate, work is dependency-driven rather than a
single toolchain ladder:

1. finish bootstrap-sufficient cross tools against real selected workloads;
2. establish the bare PDP-11 substrate: vectors, stack, console, trap/syscall
   entry, and a RAM-backed block/storage layer;
3. migrate the selected kernel responsibilities and tiny command corpus into
   a core-only PDP-11 UNIX test system;
4. replace RAM-backed storage with RF11/RS11 persistent disk support around
   the December 1970 transition;
5. move development capability onto the PDP-11 when evidence and practical
   capability justify it.

The repository ends with a reproducible first disk-backed PDP-11 UNIX
environment consistent with the surviving December-1970 evidence. Editor,
text-processing, and broader 1971 expansion are outside the required endpoint
and belong to a possible continuation.

## Questions the corpus-definition gate must answer

- Which local source version represents each selected responsibility?
- What is its `P7-*` provenance, and where are restoration changes recorded?
- Which semantics should be preserved, adapted, omitted, or reconstructed?
- Which details are attested, descendant evidence, or unknown?
- What KA11 instructions and assembler directives does the selected material
  actually require?
- What minimal machine interfaces must exist before each component can run?
- Which dependencies can advance on the bootstrap and UNIX tracks in
  parallel, and where must they converge?

Until those answers are recorded, do not infer the final assembler catalogue
from Stage 3 alone and do not begin kernel or command translation.
