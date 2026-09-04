# PDP-7 UNIX tool notes

This is a small operator reference for recovered commands used by the project,
not a general Unix manual. It is grounded in the checked-in PDP-7 sources under
`machines/pdp7/pdp7-unix/src/cmd/`. These commands must not be assigned
later-Unix behavior merely because their names are familiar.

## `ed`

The recovered editor is implemented by `cmd/ed1.s` and `cmd/ed2.s`. Startup
creates and opens `e.tmp`, initializes an empty line buffer, prints `edit`, and
enters its command loop. It never examines the process argument area.
Consequently, `ed as11.b` does **not** read `as11.b`; it starts an empty editor
and ignores the argument. A search then fails because there are no lines.

### File and buffer operations

- `r name` opens `name` and appends its lines after the addressed line, or
  after the current line/default end range when unaddressed. It remembers the
  supplied name in the eight-character filename buffer and prints the decimal
  count of characters read. Bare `r` reuses that remembered name; without one
  it is an error.
- `w name` creates/truncates `name`, writes the addressed range (the whole
  buffer by default), remembers the name, and prints the decimal character
  count. Bare `w` reuses the remembered name; without one it is an error.
- The editor has no modified-buffer flag or quit protection. `q` must be
  unaddressed and followed immediately by newline; it exits even if changes
  were not written.
- The editor's working text is represented by a line-address array plus text
  kept through its `e.tmp` backing file. A fresh invocation is empty. A
  successful `r` makes it loaded; edits change the editor buffer; only `w`
  makes the named destination reflect those changes.

The exact command letters dispatched by the recovered source are `a`, `c`,
`d`, `p`, `q`, `r`, `s`, `w`, newline, and `=`. Addresses support decimal
numbers, octal numbers with a leading zero, `.`, `$`, relative `+`/`-`, forward
`/pattern/`, backward `?pattern?`, and comma/semicolon ranges. Do not assume
any other command exists.

Forward search starts after dot and wraps from the end to the beginning;
backward search starts before dot and wraps from the beginning to the end.
Returning to the starting line without a match is an error. A search used as
an address sets the matched address. With physical newline as the command, the
matched line is printed (the ordinary addressed-newline path).

Substitution has the form:

```
s<delimiter>pattern<delimiter>replacement<delimiter>
```

The closing replacement delimiter must be followed immediately by physical
newline. There is no trailing `g` flag. The implementation keeps one match
span and performs one splice per addressed line, so it is not a global
all-occurrences substitution. The source implements `^` and `$` anchors;
character classes and closure code are disabled. A malformed expression takes
the error path; a correctly formed substitution with no match simply leaves
that addressed line unchanged and continues.

All editor errors converge on one behavior: print `?` followed by newline and
return to the command loop. Common causes include an unknown command, invalid
or out-of-range address, failed open/create, missing remembered filename,
malformed search/substitution, no search match, and addressed `q`. A valid
substitution whose pattern is absent is notably not an error.

Input-line editing is performed before command parsing: `#` erases one
character (without moving before the line start), and `@` kills the current
physical input line. Backspace/Delete are not substitutes.

### Safe small-edit recipe

Commands must be sent as separate physical lines, waiting for each result:

```
ed
r as11.b
/target/
p
s/old/new/
p
w
q
```

Here `r as11.b` loads and remembers the filename; the search-address newline
prints the located line, and the explicit `p` is a second unambiguous check.
After substitution, `p` verifies the current changed line. Bare `w` writes the
remembered filename. Confirm its decimal count, then send `q` separately and
wait for the shell prompt. For one or a few simple edits this real native
workflow is preferable to retransferring a large file. For broad structural
changes, transferring the authoritative repository source remains safer than
constructing a long editor script.

The precise choice among multiple possible matches on one line (beyond the
source-established single-splice behavior) still needs a tiny native
confirmation before a workflow depends on it.

## Other commands used by the project

- `ch` is implemented inside `sh`, not as a standalone later-Unix `cd`.
  It invokes `chdir` once for each simple name supplied, which is how directory
  chains are traversed. Do not substitute slash or `..` pathname assumptions.
- `cp` consumes arguments in source/destination pairs and can process multiple
  pairs in one invocation. An unpaired final name is an error. It creates the
  destination and copies the source contents; failures print the involved
  fixed-width names with `?`.
- `ln` exposes the native multi-component directory/link syscall conventions,
  including its special `li` form; it is not safe to infer the later two-path
  interface. Reuse only the already demonstrated project invocations unless
  the exact desired form has first been checked against `cmd/ln.s`.
- `rm` accepts one or more simple names and unlinks each. A failure prints the
  name followed by ` ?` and continues.
- `cat` requires one or more names; with none it prints `No files` and exits.
  It processes multiple files and reports a failed name as `name ?` before
  continuing.
- The shell first tries a command name in the current directory. If absent, it
  temporarily links the corresponding `system` entry into the current
  directory, opens it, and removes that temporary link. This explains why
  ownership/link behavior can differ from later Unix expectations.
- The installed reconstructed B workflow established by project evidence is
  `b input.b output.s`, then `as` over the required native assembly/runtime
  inputs. The recovered `as` accepts multiple source filenames, reads them in
  two internal passes, prints `I` and `II`, and creates `a.out` (plus `n.out`
  symbol material). Preserve the exact source ordering used by a known build.

All names above are PDP-7 directory entries, normally limited to the native
fixed-width naming convention. They are not examples of hierarchical paths.
