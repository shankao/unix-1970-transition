/ modern machine diagnostic: poll and echo two independent kl11 bytes
.=001000
start:
/ rx status bit 7 is the sign bit; tstb plus bpl waits for receiver done.
1:;tstb *$177560;bpl 1b
/ reading the receiver buffer consumes the first byte; save it in ram.
movb *$177562,r0
movb r0,first
/ tx status bit 7 is ready; wait before writing the transmitter buffer.
2:;tstb *$177564;bpl 2b
movb r0,*$177566
/ wait for completion so ready must clear and reassert before byte two.
3:;tstb *$177564;bpl 3b

/ repeat the complete receive/transmit path to prove a second input advances.
4:;tstb *$177560;bpl 4b
movb *$177562,r1
movb r1,second
5:;tstb *$177564;bpl 5b
movb r1,*$177566
6:;tstb *$177564;bpl 6b
/ both characters have been consumed, echoed, and drained; stop cleanly.
halt

/ separate words make the received low bytes independently inspectable.
.=001100
first:;0
second:;0
