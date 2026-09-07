/ stage 4c all-mode and bootstrap-mnemonic encoding fixture
.=001000
start:
mov r0,r1
mov (r0),(r1)
mov (r0)+,(r1)+
mov *(r0)+,*(r1)+
mov -(r0),-(r1)
mov *-(r0),*-(r1)
mov 2(r0),4(r1)
mov *6(r0),*10(r1)
mov $1,r0
mov *$177566,r0
mov target,r0
mov *target,r0
mov target,target2
movb $101,*$177566
cmp r0,r1
add r0,r1
clr r0
tst r0
tstb *$177564
asl r0
asr r0
jmp (r3)
jsr r5,(r3)
rts r5
br forward
012345
forward:
bne start
bpl forward
halt
target:
1
target2:
2
mark:
mark
.=002000
br .+0400
.=002400
br .-0376
