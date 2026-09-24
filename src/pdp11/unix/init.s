/ SPDX-License-Identifier: GPL-3.0-only
/ Initial RAM filesystem and descriptor state for the first cat command.

state=20000
fds=20062

/ Build the one-directory RAM filesystem in blocks 0, 1, and 2.
.=2000
fsinit:
mov $40000,r0
mov $1400,r1
0:;clr (r0)+
dec r1
bne 0b
mov $177770,state+4
mov $177740,state+6
mov $-1,state+2

/ inode 1: root directory, one direct pointer to block 1, 30 bytes.
mov $100036,*$40030
mov $1,*$40032
mov $-1,*$40052
mov $-1,*$40054
mov $36,*$40056

/ inode 2 and 3: separate tty input and output special files.
mov $100052,*$40060
mov $-1,*$40102
mov $-1,*$40104
mov $100045,*$40110
mov $-1,*$40132
mov $-1,*$40134

/ inode 4: read-only readme, one direct pointer to block 2, 36 bytes.
mov $100012,*$40140
mov $2,*$40142
mov $-1,*$40162
mov $-1,*$40164
mov $44,*$40166

/ Root directory entries are 16-bit inode plus an eight-byte name.
mov $2,*$41000
mov $72164,*$41002
mov $64571,*$41004
mov $156,*$41006
clr *$41010
mov $3,*$41012
mov $72164,*$41014
mov $67571,*$41016
mov $72165,*$41020
clr *$41022
mov $4,*$41024
mov $62562,*$41026
mov $62141,*$41030
mov $62555,*$41032
clr *$41034

/ These bytes are ordinary file data.  cat contains no copy of this text.
mov $42120,*$42000
mov $26520,*$42002
mov $30461,*$42004
mov $52440,*$42006
mov $64556,*$42010
mov $20170,*$42012
mov $62562,*$42014
mov $62141,*$42016
mov $72040,*$42020
mov $64550,*$42022
mov $20163,*$42024
mov $71146,*$42026
mov $66557,*$42030
mov $71040,*$42032
mov $60545,*$42034
mov $66544,*$42036
mov $27145,*$42040
mov $5015,*$42042
rts pc

/ One process owns ten three-word descriptors.  Lowest free is descriptor 2.
.=3000
fdinit:
mov $fds,r0
mov $36,r1
0:;clr (r0)+
dec r1
bne 0b
mov $6,fds
mov $2,fds+4
mov $5,fds+6
mov $3,fds+12
rts pc
