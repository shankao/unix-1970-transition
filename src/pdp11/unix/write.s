/ SPDX-License-Identifier: GPL-3.0-only
/ Console write, close, exit, and the system's mutable storage labels.

getfd=7200
iget=5000

/ write(fd,buffer,count) dispatches the ttyout special inode to KL11.
.=14000
syswrit:
mov (r5),r4
mov (r4),state+10
mov 2(r4),state+12
add $4,(r5)
jsr pc,getfd
tst r1
beq 9f
mov (r1),r2
bic $177772,r2
cmp $5,r2
bne 9f
mov 4(r1),r0
jsr pc,iget
tst r0
bne 9f
bit $40,inode
beq 9f
cmp $3,state
bne 9f
mov state+12,r2
tst r2
bpl 0f
br 9f
0:;mov r2,state+16
mov state+10,r3
beq 3f
1:;tstb *$177564
bpl 1b
movb (r3)+,*$177566
dec r2
bne 1b
2:;tstb *$177564
bpl 2b
3:;add $1,state+26
mov state+16,r0
rts pc
9:;mov $-1,r0
rts pc

/ close clears only the active flag; the final offset remains inspectable.
.=16000
sysclos:
jsr pc,getfd
tst r1
beq 0f
bit $4,(r1)
beq 0f
clr (r1)
clr r0
rts pc
0:;mov $-1,r0
rts pc

/ With no parent yet, exit closes descriptors, records success, and halts.
.=17000
sysexit:
mov fds+16,state+22
clr fds
clr fds+6
clr fds+14
mov $1,state+30
halt

/ Mutable system data remains below the 030000 user boundary.
.=20000
state:;.=state+32
inode:;.=.+30
fds:;.=.+74

/ One block buffer preserves the block-read boundary for later RF11 work.
.=26000
blockbuf:;.=.+1000
