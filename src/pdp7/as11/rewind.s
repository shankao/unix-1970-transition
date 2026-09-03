" Stage 4A B-callable input rewind helper.
" Class B reconstruction support; not surviving Bell Labs source.
"
" bl.s getc returns iflg before consulting cibufp/eibufp.  Reset the
" descriptor with the authentic seek syscall, discard that pending character,
" and make the current range empty so the next getc refills from .fin.

.rewind: .+1
   n 8
   n 7
   lac .fin
   sys seek; 0; 0
   sma
   jmp 1f
   jmp stop
1:
   dzm iflg
   lac eibufp
   dac cibufp
   jmp fetch
