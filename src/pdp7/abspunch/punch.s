" SPDX-License-Identifier: GPL-3.0-only
" Class C adapter: when run by the historical system account, replace the
" ordinary B output with the authentic dd/system/pptout special inode.

.punch: .+1
   n 8
   n 7
   lac d1
   sys close
   law 017
   sys creat; pptout
   sma
   jmp 1f
   jmp stop
1:
   dac .fout
   jmp fetch

pptout: <pp>;<to>;<ut>;040040
