/ SPDX-License-Identifier: GPL-3.0-only
/ Root-directory lookup and the single current-inode buffer.

state=20000
inode=20032

.=4000
namei:
mov $41000,r1
mov $3,r3
0:;tst (r1)
beq 1f
mov r0,r2
cmp (r2)+,2(r1)
bne 1f
cmp (r2)+,4(r1)
bne 1f
cmp (r2)+,6(r1)
bne 1f
cmp (r2)+,10(r1)
bne 1f
mov (r1),r0
rts pc
1:;add $12,r1
dec r3
bne 0b
mov $-1,r0
rts pc

.=5000
iget:
tst r0
bpl 0f
mov $-1,r0
rts pc
0:;cmp r0,$20
bpl 1f
mov r0,state
mov r0,r1
asl r1
asl r1
asl r1
mov r1,r2
asl r1
add r2,r1
add $40000,r1
mov $inode,r2
mov $14,r3
2:;mov (r1)+,(r2)+
dec r3
bne 2b
clr r0
rts pc
1:;mov $-1,r0
rts pc
