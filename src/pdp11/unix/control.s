/ SPDX-License-Identifier: GPL-3.0-only
/ PDP-7-derived access check and per-process descriptor selection.

state=20000
inode=20032
fds=20062

.=6000
access:
tst state+2
bpl 0f
clr r0
rts pc
0:;mov inode,r1
cmp state+2,inode+22
bne 1f
asr r1
asr r1
1:;bic $177774,r1
mov r0,r2
bic r1,r2
beq 2f
mov $-1,r0
rts pc
2:;clr r0
rts pc

.=7000
fassign:
mov $fds,r1
clr r0
0:;bit $4,(r1)
beq 1f
add $6,r1
add $1,r0
cmp $12,r0
bne 0b
mov $-1,r0
1:;rts pc

.=7200
getfd:
tst r0
bpl 0f
clr r1
rts pc
0:;cmp r0,$12
bpl 1f
mov r0,r1
asl r1
mov r1,r2
asl r1
add r2,r1
add $fds,r1
rts pc
1:;clr r1
rts pc
