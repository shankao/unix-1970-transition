# Core-only PDP-11 Execution and RAM Contract

## Status and evidence boundary

This document freezes the **provisional execution/memory contract v1** for
the diskless PDP-11/20 reconstruction. It is the completed result of the
core-only execution and RAM-layout research gate. It is a design input, not
implementation, and it is not recovered December-1970 PDP-11 source.

The evidence labels used here are deliberately explicit:

- **HISTORICALLY ATTESTED:** stated by contemporary hardware documentation or
  a first-hand historical account;
- **SURVIVING PDP-7 SOURCE EVIDENCE:** behavior visible in the contemporary
  listing lineages and their restored working derivatives;
- **CONSERVATIVE RECONSTRUCTION:** a project choice needed to make the lost
  pre-disk system concrete;
- **DESCENDANT EVIDENCE:** later early-PDP-11 UNIX material that constrains or
  demonstrates plausibility but is not the target system;
- **STILL UNRESOLVED:** deliberately deferred until translated code or a later
  research gate supplies the necessary measurements.

The physical CPU, TRAP, vector, and KL11 facts remain authoritative in
[`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md). The selected PDP-7
responsibilities and commands remain authoritative in
[`UNIX-MIGRATION.md`](UNIX-MIGRATION.md).

## Historical constraint and provisional memory map

**HISTORICALLY ATTESTED:** the target is a 24 KB PDP-11/20 KA11. Ritchie's
retrospective describes the earliest system while waiting for disk as using
approximately 12 KB for the operating system, a tiny user-program area, and
the remainder for RAM disk/storage. It was a test system, not a useful
production UNIX. The exact boundaries are not recovered.

**CONSERVATIVE RECONSTRUCTION:** v1 uses this octal byte-address map:

```text
000000-027777   system envelope       12 KB
030000-037777   active user area       4 KB
040000-057777   RAM storage arena      8 KB
060000          one past installed RAM
```

The corresponding symbolic contract is:

```text
SYS_BASE          000000
SYS_LIMIT         030000

USR_BASE          030000
USR_STATIC_LIMIT  036000    soft engineering budget only
USR_TOP           040000

RAM_BASE          040000
RAM_TOP           060000

RAM_BLOCK_SIZE       512    bytes
RAM_BLOCK_COUNT        16
```

The historical account motivates the 12 KB system envelope. The exact
`030000` and `040000` boundaries, the 4 KB user window, and therefore the 8 KB
RAM arena are reconstruction choices. A 4 KB window is plausibly tiny, leaves
one third of installed RAM for storage, is substantially smaller than the
later First Edition user area, gives a simple fixed execution window, and is
not contradicted by later command-size evidence. It remains subject to
empirical validation.

Within the user window, the following is a **soft design budget**, not a
hardware boundary or historical fact:

```text
030000-035777   executable/static image target, about 3 KB maximum
036000-037777   about 1 KB for stack, argument frame, loader stub,
                and small temporary/runtime workspace
initial SP      040000
```

The PDP-11 stack grows downward. A translated program that exceeds either
budget triggers explicit design review; it must not silently overflow into
the staging or stack region.

**STILL UNRESOLVED:** actual translated kernel size, command image sizes,
stack high-water marks, and argument demand. The 12 KB system envelope is a
budget to measure against, not permission to move `SYS_LIMIT` when code grows.

## Pre-disk executable and shell loader

**SURVIVING PDP-7 SOURCE EVIDENCE:** the PDP-7 shell forks, constructs
arguments near the top of user memory, copies a small loader sequence away
from the region it will overwrite, reads the command directly at fixed user
address 4096, and jumps there. It replaces the child image explicitly rather
than invoking an `exec` system call.

**CONSERVATIVE RECONSTRUCTION:** a pre-disk PDP-11 command is a raw absolute
memory image:

```text
assembly origin/load address   030000
entry point                    030000
a.out header                   none
relocation                     none
target symbol table            none
dynamic loader                 none
execution-time linker          none
```

The core-only shell-loader concept is:

1. after `fork`, the child performs redirection while the shell image remains;
2. it prepares argument strings and pointers near the high end of user memory;
3. it copies a tiny loader stub into protected high user memory;
4. it transfers control to that stub;
5. the stub reads the raw image at `USR_BASE`;
6. it rejects an image that would overwrite loader, arguments, or stack;
7. it closes the executable as appropriate;
8. it establishes the initial stack and argument frame;
9. it jumps to `030000`.

The precise stub address and byte layout are **STILL UNRESOLVED** implementation
details. Size rejection is required eventually but is not implemented here.

**DESCENDANT EVIDENCE:** the November 3, 1971 First Edition `a.out` format has
a six-word header containing an initial branch/identification word, text size,
symbol-table size, relocation-area size, data-area size, and an unused word,
and is associated with kernel `exec`. That later environment does not define
the pre-disk format. The intended transition to investigate is:

```text
pre-disk: raw fixed-address, shell-controlled replacement
    -> later persistent system: a.out plus kernel exec
```

The exact date or step at which that change occurred is **STILL UNRESOLVED**.

## Initial argument ABI

PDP-7 packed-character argument layout is machine-specific and will not be
copied mechanically.

**DESCENDANT-CONSTRAINED CONSERVATIVE RECONSTRUCTION:** commands begin with a
natural PDP-11 byte/pointer frame, placed as high as practical:

```text
SP -> argc
      argv[0] pointer
      argv[1] pointer
      ...
      zero pointer
      ... NUL-terminated byte strings
```

First Edition `exec` documents SP pointing to the count, followed by argument
pointers, with strings placed high in user core. Reusing that command ABI now
allows it to survive a later move from shell loading to kernel `exec`; it does
not prove the lost pre-disk system used it. Exact ordering and padding remain
to be fixed when `sh` is translated.

## Pre-disk syscall ABI

**SURVIVING PDP-7 SOURCE EVIDENCE:** calls use accumulator argument/result
roles, inline argument words, and ordinary `-1` error returns.

**CONSERVATIVE RECONSTRUCTION:** freeze the ABI shape, but not call numbers:

```text
source form        sys name
machine mechanism  KA11 TRAP-family instruction
primary register   R0
arguments          words immediately following the TRAP instruction
ordinary error     R0 = -1
```

R0 fills the PDP-7 accumulator's conceptual role. First Edition independently
supports inline arguments and TRAP dispatch as natural PDP-11 mechanisms, but
its carry-bit error convention is **DESCENDANT EVIDENCE** and is not adopted.
Symbolic names insulate source from allocation: **exact syscall numbers remain
unfrozen**. A future `sys` pseudo-operation waits for an intentional numeric
mapping; this gate adds no assembler feature.

The provisional PDP-7-derived calling shapes are:

```text
exit
    no inline arguments

fork
    no data arguments; two inline return continuations

smes
    R0 = target PID
    only synchronization needed by the reduced shell

open
    sys open
    name pointer
    mode
    returns fd or -1 in R0

creat
    R0 = PDP-7-derived mode/access input
    sys creat
    name pointer
    returns fd or -1 in R0

close
    R0 = fd

read
    R0 = fd
    sys read
    buffer
    count
    returns byte count or -1 in R0

write
    R0 = fd
    sys write
    buffer
    count
    returns byte count or -1 in R0

unlink
    sys unlink
    name pointer

status
    R0 = destination/status-buffer pointer
    sys status
    name pointer
    uses the surviving single-directory / NO_DD concept
```

These shapes are subject to source-level confirmation during translation.
The surface is not expanded by this contract.

## Child-first fork and cooperative residency

**SURVIVING PDP-7 SOURCE EVIDENCE:** `fork` finds a process slot, assigns its
PID, marks the parent ready/out, swaps out the parent, makes the current
in-core image the child, establishes distinct parent/child return
continuations, and returns immediately into the child. The shell's two return
positions enter the command loader only in the child.

The best reconstruction is therefore child-first, not a modern assumption
that the parent must continue first. A future PDP-11 source shape might be:

```text
sys fork
    br child_path
parent_path:
    ...
```

**DESCENDANT EVIDENCE:** First Edition uses the same general skip/branch idea,
which reinforces that it is natural on the PDP-11 without proving the lost
implementation.

**CONSERVATIVE RECONSTRUCTION:** only one user image need be resident, and no
clock-preemptive scheduler is required for the first milestone:

```text
shell forks
    -> parent state/image enters RAM backing
    -> child remains resident
    -> child redirects and manually loads a command
    -> command runs
```

If the child does not block, it exits, makes the parent runnable, and the
restored shell's later `smes` observes that the child has disappeared (an
error/`-1` result the shell may ignore). If the child blocks on a supported
event, the kernel may restore the ready parent; `smes(child)` then blocks while
the child exists, the child can be restored, and its eventual exit wakes the
parent so `smes` can retry and observe disappearance.

This derives strongly from PDP-7 `fork`, `smes`, `awake`, `exit`, and `swap`.
It provides foreground fork/wait-like behavior without periodic scheduling,
simultaneous resident users, modern `wait`, or useful background `&`.

## Compact process backing

**SURVIVING PDP-7 SOURCE EVIDENCE:** PDP-7 UNIX swaps 64 words of per-user
state plus the entire 4096-word user image. That 18-bit representation is not
copied to an 8 KB PDP-11 RAM arena.

**CONSERVATIVE RECONSTRUCTION:** kernel-resident process metadata conceptually
contains:

```text
PID/status
saved R0-R5 as required
saved SP, PC, PS
file-descriptor/open-file state
current-directory state if retained
executable/static image end
RAM-backing metadata
```

Backing storage saves only live byte ranges:

```text
lower image   [USR_BASE, image_end)
upper stack   [saved_SP, USR_TOP)
```

The unused gap is omitted. Restore reloads both ranges at their original
addresses and restores registers/control state. Exact metadata and packed-RAM
encoding are **STILL UNRESOLVED**.

**DESCENDANT EVIDENCE:** First Edition later packed the live stack down beside
the program before swap output and unpacked it after restore. This does not
recover the RAM-disk prototype, but demonstrates that compact program-plus-live
stack backing is compatible with very early PDP-11 UNIX.

## RAM arena and provisional filesystem geometry

**CONSERVATIVE RECONSTRUCTION:** `040000`–`057777` is one 8 KB physical arena
with separate logical clients:

```text
filesystem storage
process backing storage
```

A process image need not be an ordinary filesystem file. Allocation metadata
may differ, but the clients must not overlap. No fixed filesystem/swap
partition is frozen; a dynamic or small reserved-block policy awaits actual
requirements.

**DESCENDANT-CONSTRAINED CONSERVATIVE RECONSTRUCTION:** use 512-byte (256-word)
logical filesystem blocks provisionally. The lost RAM-disk geometry is not
attested. The choice is useful because First Edition persistent UNIX used
512-byte blocks, it eases later RF-backed transition, and the 8 KB arena then
contains exactly 16 blocks.

The RAM-only filesystem provisionally supports eight direct addresses:

```text
maximum direct file size = 8 * 512 = 4096 bytes
```

That equals the entire active user window, so any runnable executable fits
without an indirect block. Indirect/large-file support is deferred unless
translation demonstrates a necessary pre-disk file larger than 4 KB. The
PDP-7's smaller 64-by-18-bit-word blocks and large-file conversion are not
mechanically retained.

## Size evidence and empirical gates

**DESCENDANT EVIDENCE ONLY:** surviving/restored early-1972 media contains
approximately these later executable sizes:

```text
sh       954 bytes
ls      2010 bytes
rm        93 bytes
stat    1026 bytes
cat      134 bytes
```

Different source, headers, BSS assumptions, features, and assembler
conventions prevent treating these as reconstructed 1970 sizes or acceptance
limits. They show only that a 4 KB window is not obviously unreasonable; the
planned first `ls` is also deliberately reduced.

**STILL UNRESOLVED / EMPIRICAL GATES:** measure the translated kernel against
the approximate 12 KB envelope. For `sh`, `cat`, minimal `ls`, `rm`, and
`stat`, measure text/data image bytes, reserved/BSS need, stack high-water,
and argument space against the soft 3 KB image target and 1 KB headroom.
Investigate excess size before changing the 12/4/8 split: look first for
later functionality, unnecessary generality, large tables/buffers, translation
choices, and unsupported assumptions.

## Historical transition represented

```text
PDP-7 UNIX
    fixed user region; shell-controlled replacement; fork + smes; disk swap

    -> core-only PDP-11 conservative reconstruction
       fixed 030000 load; raw images; shell loader; fork + minimal smes;
       one resident process; compact RAM backing; RAM filesystem; no clock

    -> RF11/RS11 transition
       persistent blocks; research exec/wait, pathname, a.out introduction;
       disk-backed swapping

    -> first completed PDP-11 UNIX convergence
       modern exec/wait, full pathnames, and later documented conventions
```

The middle system is not called First Edition UNIX. Exact transition timing
remains unknown.

## Completed follow-on contract

The following questions are now provisionally resolved in
[`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md):

- a minimal PDP-11 inode and the PDP-7 inode semantics that survive;
- exact direct-address count;
- directory entry representation, including whether the later natural
  10-byte 16-bit-inode plus 8-byte-name form is justified or remains merely
  descendant evidence;
- root/single-directory and console-special-file inode representations;
- initial filesystem image and inode count;
- descriptor, open-file, in-core inode, and file-table sizes;
- a minimal process descriptor;
- free-block representation for only 16 RAM blocks;
- filesystem/process-backing allocation policy;
- the exact `status` result required by `stat`;
- total kernel-resident table RAM;
- mapping to selected `s2`/`s4`/`s5`/`s6`/`s8` algorithms;
- any resulting, workload-demonstrated assembler requirements.

That contract derives structures from PDP-7 source first and treats First
Edition structures only as descendant evidence. No implementation has begun;
the next gate is a repository-aware planning pass for the first implementation
slice.
