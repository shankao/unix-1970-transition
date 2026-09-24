/ SPDX-License-Identifier: GPL-3.0-only
/ Open one named ordinary file for reading.

namei=4000
iget=5000
access=6000
fassign=7000
state=20000

.=7400
sysopen:
mov (r5),r4
add $4,(r5)
tst 2(r4)
beq 0f
mov $-1,r0
rts pc
0:;mov (r4),r0
jsr pc,namei
tst r0
bpl 0f
rts pc
0:;jsr pc,iget
tst r0
bpl 0f
rts pc
0:;mov $2,r0
jsr pc,access
tst r0
bpl 0f
rts pc
0:;jsr pc,fassign
tst r0
bpl 0f
rts pc
0:;mov $6,(r1)
clr 2(r1)
mov state,4(r1)
mov r0,state+20
rts pc
