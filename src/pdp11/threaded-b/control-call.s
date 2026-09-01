/ Stage 3B class-B reconstruction; not surviving late-1970 source.
/ R2 is the pending-frame pointer between mark and call.

        . = 001320
f:      tst     -(r5)          / branch to threaded target when false/zero
        bne     1f
        mov     (r3),r3
        jmp     @(r3)+
1:      add     #2,r3
        jmp     @(r3)+

        . = 001360
tra:    mov     (r3),r3        / unconditional threaded target
        jmp     @(r3)+

        . = 001400
b4:     mov     -(r5),r0       / reconstructed equality, result 0 or 1
        cmp     -(r5),r0
        bne     1f
        mov     #1,r0
        br      2f
1:      clr     r0
2:      mov     r0,(r5)+
        jmp     @(r3)+

        . = 001440
mark:   mov     -(r5),r0       / function value was evaluated first
        mov     r5,r2          / pending frame; keep caller R4 for arguments
        mov     r4,(r5)+       / frame word 0: previous R4
        mov     r0,(r5)+       / word 1 temporarily holds callee stream
        jmp     @(r3)+

        . = 001500
call:   mov     2(r2),r0       / recover callee stream
        mov     r3,2(r2)       / frame word 1: caller threaded return R3
        mov     r2,r4          / activate frame only after arguments exist
        mov     r0,r3
        jmp     @(r3)+

        . = 001540
set:    mov     (r3)+,r0       / frame size in words (header included)
        asl     r0
        add     r4,r0
        mov     r0,r5
        jmp     @(r3)+

        . = 001560
a:      mov     (r3)+,r0       / automatic rvalue; byte offset operand
        add     r4,r0
        mov     (r0),(r5)+
        jmp     @(r3)+

/ This return-without-value body retains archaeological n11 materially intact.
        . = 001600
n11:    mov     r4,r5
        mov     (r5)+,r4
        mov     (r5),r3
        jmp     @(r3)+

        . = 001620
retv:   mov     -(r5),r0       / reconstructed return with expression value
        mov     r4,r5
        mov     (r5)+,r4
        mov     (r5),r3
        mov     r0,(r5)+       / replace saved R3 slot with caller result
        jmp     @(r3)+
