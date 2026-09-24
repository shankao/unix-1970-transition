/ SPDX-License-Identifier: GPL-3.0-only
/ KA11 TRAP entry and the five calls needed by the first cat command.

sysopen=7400
sysread=10000
syswrit=14000
sysclos=16000
sysexit=17000

.=1200
trapent:
mov r1,-(sp)
mov r2,-(sp)
mov r3,-(sp)
mov r4,-(sp)
mov r5,-(sp)
mov sp,r5
add $12,r5
/ The saved pc points to the first inline argument.  The preceding word is TRAP.
mov (r5),r1
mov -2(r1),r1
bic $177400,r1
cmp $1,r1
bne 0f
jsr pc,sysexit
br tret
0:;cmp $2,r1
bne 0f
jsr pc,sysopen
br tret
0:;cmp $3,r1
bne 0f
jsr pc,sysread
br tret
0:;cmp $4,r1
bne 0f
jsr pc,syswrit
br tret
0:;cmp $5,r1
bne 0f
jsr pc,sysclos
br tret
0:;mov $-1,r0
tret:
mov (sp)+,r5
mov (sp)+,r4
mov (sp)+,r3
mov (sp)+,r2
mov (sp)+,r1
rti
