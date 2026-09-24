/ SPDX-License-Identifier: GPL-3.0-only
/ Core-only PDP-11 Unix vector and boot entry.
/ Fixed origins let the small PDP-7 as11 assemble system parts separately.
/ Surviving PDP-7 s2/s4/s5/s6/s8 code is the behavioral ancestor.

fsinit=2000
fdinit=3000

/ KA11 TRAP vector.  The saved pc points to the first inline argument.
.=34
1200
0

.=1000
start:
mov $40000,sp
jsr pc,fsinit
jsr pc,fdinit
jmp *$30000
