# PDP-7 `as11` reconstruction

## Scope and evidence boundary

Participant accounts establish that a simple PDP-11 assembler was written in
B and run on the PDP-7, making a two-pass B tool historically plausible. The
exact 1970 source and language are lost. Stage 4 reconstructs the tool as class
**B** in five dependency gates; this document records only completed Stage 4A
results and the remaining plan.

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
no legitimate state was restored to retain an old hash. The image is left
uncommitted pending a meaningful later machine milestone.

The runner and session capture are class **M**. They automate observed PDP-7
behavior; they do not implement rewind semantics on the host.

## Remaining Stage 4 gates

- **4B:** language, tokenizer/parser, and two-pass symbol/local-label engine;
  no target encoding.
- **4C:** KA11 encoding and raw words checked by the Stage 2 oracle.
- **4D:** integrate and resource-test usable PDP-7 B `as11`.
- **4E:** reproduce and execute the Stage 3 nested-call gold program from
  PDP-7-produced words using class-M loading.

No 4B parser or symbol implementation has started.
