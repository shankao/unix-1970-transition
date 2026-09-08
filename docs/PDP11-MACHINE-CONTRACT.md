# Bare PDP-11/20 KA11 machine-layer contract

## Status and boundary

This document closes the research gate needed by the provisional PDP-7-derived
core-only UNIX corpus. It records the hardware contract of the 24 KB
PDP-11/20 and identifies the remaining pre-disk layout choices. It does not
reconstruct First Edition hardware organization, freeze the lost 1970 layout,
or authorize implementation.

## Fixed target and physical address space

```text
processor       PDP-11/20 KA11
installed core  24 KB = 12K 16-bit words
disk            none initially
```

The KA11 directly addresses 32K words, or 64 KB. Its upper 4K words are the
I/O page: CPU addresses `160000`–`177777` octal map to the high UNIBUS device
address area. On the Bell Labs target configuration, installed RAM naturally
occupies byte addresses `000000`–`057777`. Addresses above `057777` and below
the I/O page are nonexistent memory.

This physical fact does not assign every installed byte to a historical
purpose. Ritchie's retrospective describes approximately 12 KB occupied by
the operating system, a tiny user area, and the remainder as RAM-backed disk
or storage. Those are approximate constraints for a test system, not recovered
boundaries. The provisional shape is:

```text
low core                  vectors and system
approximately first 12KB  system envelope
above it                  small active-user execution area
remaining installed core  RAM storage and process backing
```

Exact addresses remain deliberately unfrozen. The later V1 16 KB system / 8
KB user split is descendant evidence and must not be imposed on the pre-disk
system.

## Registers, protection, and saved state

```text
R0-R5  general registers
R6     stack pointer (SP)
R7     program counter (PC)
PS     processor status
```

The PDP-11/20 KA11 has no hardware user/kernel protection modes. Its original
processor status does not provide the later current/previous mode machinery,
and there are no separate hardware user and kernel register banks. System and
user code share one physical address space and are separated by software
convention. A TRAP transfers control; it does not make a hardware privilege
transition.

The process machine-state abstraction should therefore preserve R0–R5, SP,
PC, and PS in software. This replaces rather than mechanically translates the
PDP-7 AC/MQ/auto-index save conventions.

## TRAP and system-call hardware

```text
TRAP opcodes  104400-104777
vector PC     000034
vector PS     000036
return        RTI
```

On TRAP the processor saves the old PC and PS through the currently active R6
stack, then loads PC and PS from the fixed vector. RTI restores the saved
PC/PS state. There is no automatic switch to a separate kernel stack: the
initial trap frame is on the interrupted code's current stack. Entry code must
therefore establish any system stack convention in software while preserving
the return frame.

A natural provisional syscall instruction is `104400 + call_number`, using
the low instruction bits to identify the call. This follows the KA11 mechanism
and is strongly corroborated by descendant early UNIX, but the exact lost
pre-disk ABI and number assignment remain reconstruction choices. A future
`sys` assembler pseudo-operation is likely appropriate only after that ABI is
frozen.

## Initial vectors

The provisional core-only minimum is:

| Vector | Initial responsibility |
| --- | --- |
| `000004` | CPU, bus, or stack-error handling |
| `000034`/`000036` | TRAP/system-call new PC/PS |
| `000060` | KL11 console input |
| `000064` | KL11 console output |

Other KA11 vectors exist. Power-fail handling is not required for initial
reconstruction. A line-clock vector is not initially required because the
provisional process model does not need periodic preemption. This is a scope
choice, not evidence that historical UNIX lacked clock support.

Vectors and fixed KA11 low-stack overflow/error behavior constrain low core.
The normal operating stack must not occupy the vector or very-low-core region.
Later V1 code beginning around `0400` is only descendant evidence consistent
with that constraint, not proof of the lost pre-disk placement.

## KL11 console

| Address | Register |
| --- | --- |
| `177560` | receiver/keyboard status |
| `177562` | receiver/keyboard buffer |
| `177564` | transmitter/printer status |
| `177566` | transmitter/printer buffer |

Input uses vector `000060`, output uses `000064`, and both interrupt at BR4.
Receiver done means a character is available and may request an interrupt;
transmitter ready means the output device can accept another character and may
request an interrupt.

PDP-7 `s7` remains semantic evidence for completion, blocking, queues, and
wakeup. Its device instructions are not translated mechanically. The KL11
layer will be new PDP-11-specific machine code.

Polling the KL11 is acceptable for bare-machine diagnostics. The actual
core-only UNIX machine layer targets interrupt-driven console operation;
polling must not become the final design merely because it eases bring-up.

## Scheduling boundary

The first core-only milestone does not require clock-driven preemption:

```text
resident shell
    -> fork
    -> save parent image/state in RAM backing
    -> run manually loaded child in active user area
    -> child exits
    -> restore and wake parent
```

Periodic scheduling is unnecessary for this foreground parent/child path.
Clock preemption, fair scheduling, and background execution remain separate
research when an actual workload needs them.

## RAM storage and process backing

Historical evidence does not recover RAM-disk geometry, allocation boundaries,
or the division between filesystem and inactive-process storage. Freeze only
the interfaces:

```text
active user image <-> process backing abstraction <-> RAM now / RF11 later
filesystem algorithms <-> block I/O abstraction     <-> RAM now / RF11 later
```

Process images need not be ordinary filesystem files. Filesystem storage and
inactive-process backing may be separate clients of one conceptual RAM arena.
No block size, block count, inode geometry, RAM-disk start, or swap partition
was fixed by this hardware gate. The follow-on contracts now select provisional
geometry. RF11 arrival should preserve high-level filesystem algorithms and
the block-I/O abstraction, but persistent metadata may evolve; it is not
necessarily a metadata-free backend replacement.

## Evidence classification

### Hardware and historically attested

- KA11 registers and absence of later user/kernel protection modes;
- physical address and I/O-page model;
- TRAP opcode family, fixed vector, current-stack PC/PS save, and RTI;
- KL11 registers, vectors, BR4 priority, and done/ready semantics;
- 24 KB target memory;
- approximate 12 KB OS, tiny user area, and remaining RAM-storage account.

### Conservative reconstruction

- low-core system placement;
- syscall number in the TRAP low bits;
- initial vector scope of 004/034/060/064;
- no initial clock scheduler;
- one active user image and software preservation of R0–R5/SP/PC/PS;
- shared conceptual RAM arena and replaceable storage abstractions;
- deferral of exact memory split and RAM geometry.

### Descendant evidence only

- early PDP-11 UNIX syscall entry at vector 034 and terminal vectors 060/064;
- descendant register-saving conventions around syscall entry;
- later 16 KB system / 8 KB user division;
- later `exec`, `wait`, and full pathname semantics.

Descendant details constrain comparison but are not automatically backported.

## Provisional bare-machine contract

```text
target       PDP-11/20 KA11, 24 KB installed core
registers    R0-R5, SP=R6, PC=R7, PS
protection   no hardware UNIX user/kernel mode separation
syscalls     TRAP 104400-104777, vector 034/036,
             current-stack PC/PS save, RTI return
console      KL11 at 177560/2 and 177564/6,
             vectors 060/064, BR4
vectors      initially 004, 034, 060, 064
scheduling   no periodic clock required initially
memory       low system, small active-user window, remaining RAM backing;
             exact split unfrozen
storage      abstract filesystem/process backing, RAM initially, RF11 later
```

## Layout question handed to the follow-on contract

This hardware gate left the necessary active pre-disk user size unresolved; it
could not select an arbitrary historical number. The completed follow-on
contract now chooses a provisional 4 KB window from the minimal commands,
loader, stack/data, backing, kernel-budget, and RAM-storage constraints. That
choice remains reconstruction subject to translated-size measurements, not a
new hardware fact.

## Completed follow-on contract

The research items below are now provisionally frozen in
[`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md):

- initial PDP-11 executable-image representation and command load address;
- active-user window size and stack placement;
- shell/manual command-loader mechanics;
- process-image save/restore layout;
- syscall argument/result convention;
- estimated sizes of `sh`, `cat`, minimal `ls`, `rm`, and `stat`;
- estimated kernel size against the approximate 12 KB historical envelope;
- RAM remaining for filesystem and process backing;
- whether direct-block-only files suffice;
- only then, a conservative RAM block geometry if one is needed.

No machine-layer implementation has begun. The filesystem/data-structure
follow-on is now provisionally frozen in
[`PDP11-FILESYSTEM-CONTRACT.md`](PDP11-FILESYSTEM-CONTRACT.md); the next gate
is repository-aware planning for the first implementation slice.
