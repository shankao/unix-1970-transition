/ class b/m diagnostic for vectors, kl11 interrupts, rti, and trap entry
/ low-core words are hardware vectors: handler pc followed by priority-four ps.
.=34
trapent
0
.=60
rxint
200
txint
200

.=1000
/ a normal high stack leaves low core exclusively for vectors and trap frames.
mov $27000,sp
/ receiver interrupt enable is bit 6; done remains the hardware-owned bit 7.
mov $100,*$177560
1:;tst done;bpl 1b
clr *$177560

/ trap 7 is diagnostic only. its inline word is consumed by the handler.
mov $12345,r1
mov $65432,r2
trap 7
12345
mov r0,trapres
cmp r1,$12345;bne fail
cmp r2,$65432;bne fail
mov $1,success
halt
fail:;mov $-1,success;halt

.=2000
/ receiver isr records the untouched hardware frame before saving r0 itself.
rxint:;mov (sp),savedpc;mov 2(sp),savedps;mov r0,-(sp)
add $1,rxints
movb *$177562,r0
tst rxcount;bne 2f
movb r0,first;br 3f
2:;movb r0,second
3:;add $1,rxcount;movb r0,txchar;mov $-1,txpend
/ enabling tx interrupt while ready starts the interrupt-driven output path.
mov $100,*$177564
mov (sp)+,r0
rti

/ first tx interrupt writes; the completion interrupt disables ie and counts it.
txint:;mov r0,-(sp);add $1,txints
tst txpend;bpl 4f
movb txchar,*$177566
clr txpend
br 5f
4:;clr *$177564;add $1,txcount;cmp txcount,$2;bne 5f
mov $-1,done
5:;mov (sp)+,r0;rti

/ trap frame pc points at the inline argument. advance saved pc before rti.
trapent:;mov r1,-(sp);mov r2,-(sp)
mov 4(sp),r0
mov -2(r0),r1;bic $177400,r1;mov r1,txchar
mov (r0)+,r2;mov r0,4(sp);add r1,r2;mov r2,trapres
mov (sp)+,r2;mov (sp)+,r1;mov trapres,r0;rti

.=3000
rxcount:;0
txpend:;0
txchar:;0
txcount:;0
done:;0
first:;0
second:;0
savedpc:;0
savedps:;0
rxints:;0
txints:;0
trapres:;0
success:;0
