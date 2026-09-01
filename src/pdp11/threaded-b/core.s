/ Stage 3A readable reconstruction; this file is not assembled in Stage 3A.
/ PDP-11 byte addresses. R3=thread PC, R4=display/frame, R5=expression stack.

        . = 001000
start:  mov     #STREAM,r3     / selected by modern deposit harness
        mov     #004000,r4     / synthetic frame
        mov     #005000,r5     / expression stack
        jmp     @(r3)+

/ c, x, va, b12, and b1 closely reproduce Thompson's documented operators.
        . = 001100
c:      mov     (r3)+,(r5)+
        jmp     @(r3)+

        . = 001120
x:      mov     @(r3)+,(r5)+
        jmp     @(r3)+

        . = 001140
va:     mov     (r3)+,r0
        add     r4,r0
        asr     r0
        mov     r0,(r5)+
        jmp     @(r3)+

        . = 001160
b12:    add     -(r5),-2(r5)
        jmp     @(r3)+

        . = 001200
b1:     mov     -(r5),r0
        mov     -(r5),r1
        asl     r1
        mov     r0,(r1)
        mov     r0,(r5)+
        jmp     @(r3)+

/ Project test support, not a documented original B operator.
        . = 001240
emit:   mov     -(r5),r0
1:      tstb    @#177564
        bpl     1b
        movb    r0,@#177566
2:      tstb    @#177564       / ensure queued character completes before HALT
        bpl     2b
        jmp     @(r3)+

        . = 001300
stop:   halt

/ Modern harness streams (operator addresses and operands, not instructions):
/ A: c;0100; c;1; b12; emit; stop
/ B: x;003000; emit; stop
/ C: c;001401; c;0103; b1; emit; stop  (001401 = 003002 / 2)
/ D: va;4; c;0104; b1; emit; stop
