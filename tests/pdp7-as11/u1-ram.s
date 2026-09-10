/ class b/m diagnostic for the shared sixteen-block ram storage primitive
.=1000
mov $27000,sp
/ map reserved metadata blocks for block io, but never return them from alloc.
mov $0,r0;jsr r4,baddr;cmp r0,$40000;bne fail
mov $20,r0;jsr r4,baddr;cmp r0,$-1;bne fail
mov $0,r0;jsr r5,freeblk;cmp r0,$-1;bne fail

/ allocate every dynamic block; block numbers 2 through 17 must be distinct.
mov $allocs,r3
mov $0,r4
1:;jsr r5,alloc;mov r0,(r3)+;add $1,r4;cmp r4,$16;bne 1b
jsr r5,alloc
mov r0,exhaust
cmp r0,$-1;bne fail

/ fill one complete 512-byte kernel buffer with a deterministic word pattern.
mov $buffer,r3
mov $0,r4
6:;mov r4,(r3)+;add $1,r4;cmp r4,$400;bne 6b
mov $65432,*$43000
mov $2,r0;mov $buffer,r1;jsr r5,bwrite

/ clear, read back, compare all 256 words, and preserve the next block sentinel.
mov $buffer,r3
mov $400,r4
7:;clr (r3)+;add $-1,r4;bne 7b
mov $2,r0;mov $buffer,r1;jsr r5,bread
mov $buffer,r3
mov $0,r4
8:;cmp (r3)+,r4;bne fail;add $1,r4;cmp r4,$400;bne 8b
cmp *$43000,$65432;bne fail

/ freeing and reallocating block 2 also models a process-backing pool claimant.
mov $2,r0;jsr r5,freeblk;cmp r0,$0;bne fail
jsr r5,alloc
mov r0,procblk
cmp r0,$2;bne fail
mov $1,success
halt
fail:;mov $-1,success;halt

.=2000
/ freemap bit one means available; bits zero and one stay reserved.
alloc:;mov freemap,r0;mov $4,r1;mov $2,r2
2:;bit r1,r0;bne 3f;asl r1;add $1,r2;cmp r2,$20;bne 2b
mov $-1,r0;rts r5
3:;bic r1,freemap;mov r2,r0;rts r5

/ validate a block number by scanning only the dynamic range before freeing it.
freeblk:;mov r0,r3;mov $4,r1;mov $2,r2
4:;cmp r2,r3;bne freecont;bis r1,freemap;mov $0,r0;rts r5
freecont:;asl r1;add $1,r2;cmp r2,$20;bne 4b
mov $-1,r0;rts r5

/ convert a checked logical block number into its 512-byte ram address.
baddr:;mov r0,r3;mov $0,r2;mov $40000,r0
5:;cmp r2,r3;bne badnext;rts r4
badnext:;add $1,r2;add $1000,r0;cmp r2,$20;bne 5b
mov $-1,r0;rts r4

/ one-buffer block abstraction; these copy exactly 256 words in either direction.
bwrite:;jsr r4,baddr;mov r1,r3;mov $400,r2
9:;mov (r3)+,(r0)+;add $-1,r2;bne 9b;rts r5
bread:;jsr r4,baddr;mov r1,r3;mov $400,r2
0:;mov (r0)+,(r3)+;add $-1,r2;bne 0b;rts r5

.=3000
freemap:;177774
allocs:;0;0;0;0;0;0;0;0;0;0;0;0;0;0
exhaust:;0
procblk:;0
success:;0

/ the runtime touches the full 512-byte range beginning here.
.=5000
buffer:;0
