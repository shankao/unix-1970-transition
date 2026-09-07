/ stage 3 shaped bootstrap workload: 17 globals and five numeric locals
.=001000
start:
mov $stream,r3
mov $frame,r4
mov $stack,r5
jmp *(r3)+
c:;mov (r3)+,(r5)+;jmp *(r3)+
x:;mov *(r3)+,(r5)+;jmp *(r3)+
va:;mov (r3)+,r0;add r4,r0;asr r0;mov r0,(r5)+;jmp *(r3)+
b12:;add -(r5),-2(r5);jmp *(r3)+
b1:;mov -(r5),r0;mov -(r5),r1;asl r1;mov r0,(r1);mov r0,(r5)+;jmp *(r3)+
emit:;tstb *$177564;bpl emit;movb r0,*$177566;jmp *(r3)+
stop:;halt
poll:;clr r0;tst r0;bne done;br poll
done:;cmp r0,r1
br 0f;0:
1:;bne 1b
br 2f;2:
3:;bpl 3b
br 4f;4:
ext:;0102
target:;0
frame:;0
stack:;0
stream:;c;0100;c;1;b12;emit;stop
mark:;start
table:;x;ext;va;4;b1;target
