/ SPDX-License-Identifier: GPL-3.0-only
/ Ordinary-file read through a direct RAM block and one kernel buffer.

getfd=7200
iget=5000
pget=12000
bread=13000
state=20000
inode=20032
blockbuf=26000

.=10000
sysread:
mov (r5),r4
mov (r4),state+10
mov 2(r4),state+12
add $4,(r5)
jsr pc,getfd
tst r1
beq 9f
mov (r1),r2
bic $177771,r2
cmp $6,r2
bne 9f
mov r1,state+14
mov 4(r1),r0
jsr pc,iget
tst r0
bne 9f
bit $40,inode
bne 9f
mov inode+26,r3
mov state+14,r1
sub 2(r1),r3
tst r3
bpl 0f
br 9f
0:;beq 8f
mov state+12,r2
tst r2
bpl 1f
br 9f
1:;beq 8f
cmp r3,r2
bpl 2f
mov r3,r2
2:;mov r2,state+16
mov 2(r1),r0
jsr pc,pget
tst r0
bpl 3f
br 9f
3:;mov $blockbuf,r1
jsr pc,bread
tst r0
bne 9f
mov state+14,r1
mov 2(r1),r3
bic $177000,r3
mov $1000,r2
sub r3,r2
cmp r2,state+16
bpl 4f
mov r2,state+16
4:;mov $blockbuf,r4
add r3,r4
mov state+10,r3
mov state+16,r2
5:;movb (r4)+,(r3)+
dec r2
bne 5b
mov state+14,r1
add state+16,2(r1)
add $1,state+24
mov state+16,r0
rts pc
8:;clr r0
rts pc
9:;mov $-1,r0
rts pc
