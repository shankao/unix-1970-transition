/ stage 3b test l: nested threaded-b call, expected console output d
/ all addresses are pdp11 byte addresses; assembled natively by pdp7 as11
.=001000
start:
mov $stream,r3
mov $004000,r4
mov $005000,r5
jmp *(r3)+

.=001100
c:;mov (r3)+,(r5)+;jmp *(r3)+

.=001120
x:;mov *(r3)+,(r5)+;jmp *(r3)+

.=001140
va:;mov (r3)+,r0;add r4,r0;asr r0;mov r0,(r5)+;jmp *(r3)+

.=001160
b12:;add -(r5),-2(r5);jmp *(r3)+

.=001200
b1:;mov -(r5),r0;mov -(r5),r1;asl r1;mov r0,(r1);mov r0,(r5)+;jmp *(r3)+

.=001240
emit:
mov -(r5),r0
1:;tstb *$177564;bpl 1b
movb r0,*$177566
2:;tstb *$177564;bpl 2b
jmp *(r3)+

.=001300
stop:;halt

.=001320
f:
tst -(r5)
bne 1f
mov (r3),r3
jmp *(r3)+
1:;add $2,r3;jmp *(r3)+

.=001360
tra:;mov (r3),r3;jmp *(r3)+

.=001400
b4:
mov -(r5),r0
cmp -(r5),r0
bne 3f
mov $1,r0
br 4f
3:;clr r0
4:;mov r0,(r5)+;jmp *(r3)+

.=001440
mark:
mov -(r5),r0
mov r5,r2
mov r4,(r5)+
mov r0,(r5)+
jmp *(r3)+

.=001500
call:
mov 2(r2),r0
mov r3,2(r2)
mov r2,r4
mov r0,r3
jmp *(r3)+

.=001540
set:
mov (r3)+,r0
asl r0
add r4,r0
mov r0,r5
jmp *(r3)+

.=001560
a:
mov (r3)+,r0
add r4,r0
mov (r0),(r5)+
jmp *(r3)+

.=001600
n11:
mov r4,r5
mov (r5)+,r4
mov (r5),r3
jmp *(r3)+

.=001620
retv:
mov -(r5),r0
mov r4,r5
mov (r5)+,r4
mov (r5),r3
mov r0,(r5)+
jmp *(r3)+

.=002540
stream:
c
fnouter
mark
c
0103
call
emit
stop

.=003240
fnouter:
set
3
c
fninner
mark
a
4
call
c
1
b12
retv

.=003300
fninner:
set
3
a
4
retv
