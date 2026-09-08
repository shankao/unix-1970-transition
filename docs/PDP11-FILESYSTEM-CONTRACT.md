# Core-only Filesystem and Kernel Data-Structure Contract

## Status and evidence boundary

This document freezes the **provisional core-only filesystem and kernel
data-structure contract v1** for the diskless PDP-11/20 reconstruction. It is
sufficiently constrained to begin repository-aware implementation planning;
it is not recovered December-1970 PDP-11 source or proof of the exact lost
layout. No structure or algorithm is implemented by this gate.

Evidence is labelled throughout:

- **HISTORICALLY ATTESTED:** contemporary documentation or first-hand account;
- **SURVIVING PDP-7 SOURCE EVIDENCE:** behavior in the listing lineage;
- **RESTORED PDP-7 SOURCE:** working derivatives used to inspect that behavior;
- **CONSERVATIVE RECONSTRUCTION:** a project choice for the lost pre-disk
  PDP-11 system;
- **DESCENDANT EVIDENCE:** later PDP-11 UNIX evidence that constrains but does
  not specify this target;
- **UNRESOLVED:** deliberately left for measurements or implementation design.

The migration workload, machine boundary, and 12/4/8 KB execution partition
remain authoritative in [`UNIX-MIGRATION.md`](UNIX-MIGRATION.md),
[`PDP11-MACHINE-CONTRACT.md`](PDP11-MACHINE-CONTRACT.md), and
[`PDP11-EXECUTION-CONTRACT.md`](PDP11-EXECUTION-CONTRACT.md).

## Per-process open files

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** `s8.s` gives each swappable
64-word `userdata` ten open-file records in `u.ofiles`. Each three-word
`fnode` holds flags, offset, and inode number. `s5.s:fassign` scans descriptors
0 through 9 and returns the lowest free slot. The shell can consequently use:

```text
close(0); open(...)   -> 0
close(1); creat(...)  -> 1
```

for redirection. This behavior is part of the selected interface, not an
incidental implementation detail.

**CONSERVATIVE RECONSTRUCTION:** retain ten descriptors in each PDP-11 process
record, each three 16-bit words:

```text
f.flags   active, read, and write bits
f.offset  byte offset
f.inum    inode number
```

Allocation remains lowest-free. `fork` copies the descriptor array with the
rest of the process state. Parent and child therefore have copied descriptor
records; they do not share a later-style open-file description. Core-only v1
has no global open-file table. That transitional semantic difference must not
be silently modernized.

## One current inode

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** the kernel has `ii`, the current
inode number, and one `inode` working buffer. `iget` fills it and `iput` writes
it back. It does not require a modern resident-inode cache for the selected
path.

**CONSERVATIVE RECONSTRUCTION:** core-only v1 keeps one current inode-number
variable and one 24-byte inode buffer. It has no inode cache, inode
reference-count table, vnode layer, or global open-file table. The cooperative
single-resident execution model makes that simplification sufficient.

## Inode v1

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** a PDP-7 inode is twelve 18-bit
words: flags; seven block pointers; uid; negative link count; word size; and a
unique number. Relevant semantics include allocation, directory and special
types, owner/other access bits, direct blocks, uid, negative links, size, and
the unique-number mechanism. Large/indirect files are outside the selected
core-only workload.

**CONSERVATIVE RECONSTRUCTION:** retain the twelve-word shape using PDP-11
words, but adapt the contents:

```text
word 0       flags
words 1-8    eight direct RAM-block numbers
word 9       16-bit uid
word 10      negative link count
word 11      16-bit size in bytes

total        12 words / 24 bytes
```

The PDP-7 unique-number word is removed and its seventh pointer expands to
eight direct pointers. Eight 512-byte blocks yield a 4096-byte maximum file,
equal to the provisional active-user window. There is no large-file flag,
indirection, or conversion before RF11 unless a real migration workload
disproves this choice.

### Unique number

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** `i.uniq`, `d.uniq`, and `s.uniq`
exist; create/link code transfers the value between inode and directory entry.
On the selected path, however, `namei` matches nonzero inode number and name,
while `open`, `read`, `write`, `close`, `unlink`, and `status` do not require
the unique value. `link` is deferred.

Omitting it is a **CONSERVATIVE REMOVAL OF AN UNNEEDED PDP-7 MECHANISM**, not
proof that the historical pre-disk PDP-11 omitted it. A translated dependency
must reopen the decision.

### Flags and access

**CONSERVATIVE RECONSTRUCTION constrained by PDP-7 source:** use a 16-bit flag
word with these conceptual values:

```text
allocated       0100000
special         0000040
directory       0000020
owner read      0000010
owner write     0000004
other read      0000002
other write     0000001
```

The high/sign bit marks allocation; the low permission/type values retain the
PDP-7 organization. The `access` responsibility can remain close to its source:
negative uid bypasses access checks; otherwise select owner bits when current
uid equals inode uid, then compare requested bits. Keep a 16-bit uid. The
directly started shell may initially use uid `-1`, as the PDP-7 startup
`userdata` does. Permissions remain structurally meaningful without adding
login/password machinery.

### Negative link count and byte size

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** creation sets `i.nlks=-1`, link
decrements farther, and unlink increments toward zero; reaching zero frees the
inode and blocks.

**CONSERVATIVE RECONSTRUCTION:** preserve that negative representation even
though `link` is initially absent. Ordinary files start at `-1`, keeping
unlink/lifetime logic close to the predecessor. A later persistent system may
migrate to documented positive counts.

File size changes from PDP-7 words to a 16-bit byte count. That architectural
adaptation is required by byte-native PDP-11 commands and I/O; 4096 bytes fits
comfortably. PDP-7 packed 9-bit-character size conventions do not survive.

## Directory v1

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** `dnode` is fixed size and carries
an inode number, an eight-character name in four PDP-7 words, unique value,
and padding to eight words. Inode number zero marks a free entry. Selected
`namei` behavior compares nonzero inode number and filename, not the unique
value.

**CONSERVATIVE RECONSTRUCTION, strongly corroborated by DESCENDANT EVIDENCE:**

```text
bytes 0-1   16-bit inode number; zero means free
bytes 2-9   fixed, NUL-padded eight-byte filename
total       10 bytes
```

Maximum filename length is eight bytes. The November 1971 First Edition
directory independently has exactly a 16-bit inode plus eight-byte NUL-padded
name, but that does not recover the pre-disk representation. The continuity is
PDP-7 inode-plus-eight-character name, natural byte-native PDP-11 adaptation,
then later documented 10-byte format.

Core-only v1 has one directory in fixed RAM block 1. It holds
`floor(512/10)=51` entries with two bytes unused. It never expands and has no
subdirectories, pathnames, `.` or `..`. `dslot` finds the first zero-inode
entry, or appends a record while the recorded directory size remains within
one block. These omissions must not be confused with later First Edition
conventions.

## Status result

**SURVIVING/RESTORED PDP-7 SOURCE EVIDENCE:** `status` copies the twelve-word
inode followed by the inode number, thirteen words total. `stat.s` consumes
that compact layout.

**CONSERVATIVE RECONSTRUCTION:** retain thirteen 16-bit words / 26 bytes:

```text
word 0       flags
words 1-8    direct block numbers
word 9       uid
word 10      negative link count
word 11      byte size
word 12      inode number
```

The first PDP-11 `stat` need display only inode number, flags, uid, link count,
and size. First Edition's later 34-byte stat result and timestamps are
**DESCENDANT EVIDENCE**, not imported.

Likewise, the richer First Edition 32-byte persistent inode—with eight
addresses, byte size, positive link count, uid, times, and additional
persistent semantics—is evidence of later evolution. Core-only v1 has no
creation/modification times, persistent mount or allocation metadata,
large-file indirection, or V1 inode wholesale.

## Physical RAM organization

The execution contract already provisionally freezes an 8 KB arena of sixteen
512-byte blocks. **CONSERVATIVE RECONSTRUCTION:** organize it as:

```text
block 0       inode storage
block 1       fixed root-directory data
blocks 2-15   common dynamic filesystem/process-backing arena
```

### Inode block

Freeze sixteen inode slots. Sixteen 24-byte records consume 384 bytes of
block 0; its remaining 128 bytes acquire no speculative historical metadata.
Inode zero remains invalid/free-marker context as appropriate. Root and device
inode numbers are **UNRESOLVED image-building choices**, not historical facts.

### Initial namespace and console files

Conceptually seed separate console-input and console-output special files,
`cat`, `ls`, `rm`, `stat`, and fixture files. The shell starts directly at
cold start. Keeping a `sh` executable in RAM storage is preferred only if
measured capacity permits; boot/core initialization may instead preload the
initial shell as process 1.

Names analogous to PDP-7 `ttyin` and `ttyout` are preferred because they
preserve separate read/write responsibilities. Do not add `/dev` or pathname
structure. Exact initial inode assignments and the decision to store `sh` are
**UNRESOLVED**.

Special inodes have no data blocks. Ordinary `read` on the input inode
dispatches to KL11 input; ordinary `write` on the output inode dispatches to
KL11 output. A small mapping keyed by inode number is enough; no generalized
major/minor device framework is introduced.

The initial shell descriptor state is:

```text
fd 0     read-open console-input special inode
fd 1     write-open console-output special inode
fd 2-9   free
```

Lowest-free allocation and descriptor copying make PDP-7-style redirection
and child inheritance follow naturally.

## Process records and compact backing

**CONSERVATIVE RECONSTRUCTION:** limit the first system to two process slots,
shell parent and command child. Preserve conceptual states without copying
PDP-7 numeric encodings or its packed disk-address status word:

```text
free
resident/ready
resident/blocked
backed/out/ready
backed/out/blocked
```

Reserve 64 PDP-11 words / 128 bytes per process, intentionally echoing the
PDP-7 64-word `userdata` scale without claiming the lost PDP-11 used this
layout. Each record has room for:

```text
state, pid, smes target/wait pid
uid, current-directory inode
kernel resume/continuation
R0-R5, saved SP, PC, PS
lower live-image size, upper live-stack size
backing-block count and up to eight block numbers
ten three-word descriptor records
small reserve
```

Exact word offsets remain **UNRESOLVED** until assembly defines symbolic
offsets.

Compact backing retains the execution contract: pack `[USR_BASE,image_end)`
then `[saved_SP,USR_TOP)` consecutively into 512-byte blocks, omitting the
unused gap. The process record holds the lengths and at most eight block
numbers; restore puts both ranges back at their original addresses and restores
machine state. Actual shell backing should use fewer than the maximum, but
only measurement can establish that.

## Shared allocators

**CONSERVATIVE RECONSTRUCTION:** use one 16-bit RAM-block availability map,
one bit per arena block. Blocks 0 and 1 are permanently unavailable; blocks
2–15 may belong to either an inode direct-pointer array or a process
backing-block list, never both. Freeing either returns it to the common map.
No separate ownership table is needed. Bit polarity remains implementation
tunable; `1 = free` is a reasonable convention and has descendant
corroboration.

Use a second 16-bit inode availability map. `icreat` becomes conceptually:

```text
find free inode bit
mark allocated
set flags and uid
set nlinks = -1 and size = 0
clear eight direct pointers
install directory entry
```

This preserves PDP-7 allocation responsibilities without scanning disk inodes.

Do not port the PDP-7 cached/chained disk free list. Preserve only allocation
semantics: acquire an unused block, zero a new filesystem data block, release
blocks on truncation/unlink, and fail cleanly when exhausted. The bitmap is a
natural tiny-RAM replacement; First Edition's later bitmap is corroboration,
not proof of the lost design.

## Direct files and filesystem layers

Freeze eight direct pointers and no indirection. `pget` reduces conceptually
to:

```text
logical_block = byte_offset / 512
require logical_block < 8
allocate and zero a block if a writing operation needs an absent pointer
return the RAM block number
```

The selected layers remain:

```text
iget/iput     inode slots in block 0
dget/dput     10-byte directory records in block 1
pget          direct logical-file-block mapping
iread/iwrite  byte-stream file access
```

This preserves responsibilities, not PDP-7 instruction flow.

Reserve one 512-byte kernel block buffer and retain an abstract
`bread(block,buffer)` / `bwrite(block,buffer)` boundary even though RAM could
be accessed directly. One buffer suffices for a cooperative direct-only
system and leaves a clean RF11 device boundary without copying PDP-7's
multi-buffer disk machinery.

## Console queue and wait state

Only the semantics of the PDP-7 queue/wakeup design survive. The PDP-11 is
byte-addressable and has one console, so its linked two-word character-node
pool is not copied.

**CONSERVATIVE RECONSTRUCTION:** use a small byte-oriented input ring so an
interrupt can accept input while user code is elsewhere and wake a blocked
reader. About 64 bytes is a reasonable scale comparable to the predecessor,
but remains **IMPLEMENTATION-TUNABLE**, not a frozen historical capacity.
Output needs only one current/pending transmitter character plus blocked-state
wakeup for the first system.

A small wait mask covers tty input and tty output, analogous in purpose to
PDP-7 `sfiles`. Keep `smes`'s target PID separately in its process record. No
general sleep-channel framework is required unless actual translation proves
it simpler.

## Resident-data budget

**PRELIMINARY RECONSTRUCTION CALCULATION, not a fit result:**

```text
one block buffer                         512 bytes
two 64-word process records              256 bytes
current inode plus inode-number state    about 26 bytes
current directory entry/index            about 12 bytes
two allocation maps                        4 bytes
tty input/wait state                     small
syscall/filesystem scratch               small
```

The obvious mutable resident data is under approximately 1 KB before code and
unforeseen tables. This keeps the historically approximate 12 KB system
envelope plausible from a data-structure perspective; it does not demonstrate
that the assembled kernel fits.

## RAM capacity invariant

The fourteen dynamic blocks must hold command/test files and parent backing
during child execution. Every initial image must satisfy:

```text
reserved metadata/root blocks
+ initial filesystem blocks
+ worst-case shell backing blocks
+ minimal writable-test headroom
<= 16 blocks total
```

After reserving blocks 0 and 1, enough must remain to back the resident shell,
run a child whose executable already occupies filesystem blocks, and create at
least one small redirection/unlink test file. Command sizes are not frozen.
If measurements fail, reconsider whether `sh` must be stored, command feature
size, the user-window split, and the filesystem corpus before changing the
historical memory envelope.

## RF11 transition boundary

The strong invariant is narrower than “replace the RAM backend unchanged”:

```text
high-level filesystem algorithms and the block-I/O abstraction should survive
RF11 arrival; persistent filesystem metadata may evolve
```

The RAM prototype need not imitate First Edition superblock/free maps, inode
map, richer inode, timestamps, mount state, root/pathname conventions, or other
persistent metadata merely to make RF11 a zero-change transition. Those may
legitimately emerge during RF11/early-1971 convergence.

## Workload-derived assembler implications

This gate reinforces future needs already derived from the migration corpus:

```text
byte operations       movb cmpb clrb
bit manipulation      bit bic bis
arithmetic/control    inc dec add sub shifts comparison branches
```

Pointer increments, addition, and shifts suffice: small nonnegative offsets
can be divided by 512 by shifting; word pointer indexes use `asl`; directory
and inode traversal add 10 and 24. No EIS multiply/divide is justified.

Inspection of the current Stage-4B/4C expression engine shows only unary `-`
and binary `+`/`-`; it has no equivalent unary bitwise complement. Natural
KA11 masking with BIC exposes unary expression complement, in forms analogous
to `$!mask`, as a **strongly justified future assembler-language feature**.
This contract does not implement it or any instruction/directive.

## Compact v1 summary

```text
RAM arena       16 x 512-byte blocks
block 0         16 x 24-byte inode slots
block 1         one fixed root directory
blocks 2-15     common filesystem/process-backing allocation

inode           12 words: flags, 8 direct blocks, uid,
                negative nlinks, byte size
directory       10 bytes: 16-bit inum + 8-byte NUL-padded name
files           4096 bytes maximum; no indirect blocks
status          12-word inode image + inum = 13 words / 26 bytes

processes       2 slots; 64-word record each provisionally
descriptors     10 per process; 3 words each; lowest-free
inode cache     none; one current inode buffer
open-file table none
tty             separate input/output special-file semantics
allocation      16-bit block map + 16-bit inode map
block buffer    one 512-byte kernel buffer
```

## Completed repository-aware integration and next slice

The repository-aware inspection is complete. It established:

- exact Stage-4C assembler syntax/features, including complement and data
  directive status;
- current PDP-11 execution harness, Stage-3 loading/transfer path, artifacts,
  and oracle integration;
- the smallest real Unix-derived machine-layer component;
- exact dependency order for vectors, trap entry, KL11 polling proof, KL11
  interrupts, RAM/block abstraction, filesystem nucleus, process control, and
  shell/commands;
- non-speculative tests available at each boundary;
- the point where a first persistent PDP-11 era becomes meaningful.

The separately authorized Stage-3 gold integration now proves the PDP-7
`as11` word path, and the KL11 polling input/output diagnostic is complete.
The next bounded implementation slice is low-core vectors/RTI, followed by
interrupt-driven console. Filesystem implementation remains unstarted.
