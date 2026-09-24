/ SPDX-License-Identifier: GPL-3.0-only
/ Direct-block lookup and a 512-byte RAM block read.

inode=20032

.=12000
pget:
mov r0,r1
asr r1
asr r1
asr r1
asr r1
asr r1
asr r1
asr r1
asr r1
asr r1
cmp r1,$10
bpl 1f
asl r1
add $inode+2,r1
mov (r1),r0
tst r0
bne 2f
1:;mov $-1,r0
2:;rts pc

.=13000
bread:
tst r0
bpl 0f
mov $-1,r0
rts pc
0:;cmp r0,$20
bpl 3f
mov r0,r2
asl r2
asl r2
asl r2
asl r2
asl r2
asl r2
asl r2
asl r2
asl r2
add $40000,r2
mov r1,r3
mov $400,r4
2:;mov (r2)+,(r3)+
dec r4
bne 2b
clr r0
rts pc
3:;mov $-1,r0
rts pc
