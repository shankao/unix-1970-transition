/ comments only before the first statement ; ignored separator
.=[0+0] / grouping in a resolvable location assignment
.=001000; base=7
start:
012345 / comment ; this must be ignored
forward
.+2
-base+[2+3]
1f; 1:; 1b; 1f; 1:; 1b
2f; 3f; 2:; 2b; 3:; 3b
forward:
start+2
longnamex=1
longnamey=2
longnamex
base=10
base
foo:; 1
bar:; foo+2
alpha=20
alpha-1+2
[alpha-[3+1]]+1
4f
4:
4b
/ padding makes this source cross the 128-character B input refill boundary
