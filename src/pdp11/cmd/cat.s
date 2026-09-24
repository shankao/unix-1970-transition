/ SPDX-License-Identifier: GPL-3.0-only
/ PDP-11 translation of the surviving PDP-7 cat command's central loop.
/ The first loader supplies one fixed name because argv and the shell are later.

sxexit=1
sxopen=2
sxread=3
sxwrite=4
sxclose=5

.=30000
start:
/ open readme for reading; fd 0 and 1 are already the two console files.
trap sxopen
readme
0
tst r0
bpl opened
trap sxexit

opened:;mov r0,r3
catloop:
/ Read eight bytes at a time, preserving the PDP-7 command's buffered shape.
mov r3,r0
trap sxread
buffer
10
tst r0
bne catwrite

/ EOF closes the input descriptor before the command exits.
mov r3,r0
trap sxclose
trap sxexit

catwrite:
/ The inline write count is patched with the short final read, as on PDP-7.
mov r0,wcount
mov $1,r0
trap sxwrite
buffer
wcount:;0
br catloop

/ Fixed eight-byte, NUL-padded name used by the one-directory namei.
readme:;62562;62141;62555;0

/ The kernel copies ordinary-file bytes here.  The command has no output text.
.=37000
buffer:;.=.+10
