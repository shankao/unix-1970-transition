/* SPDX-License-Identifier: GPL-3.0-only
 * Class C reconstruction of a PDP-7-side DEC PDP-11 absolute-tape writer.
 * Input is the native as11 i/x/w trace; output goes to the PDP-7 punch.
 */
main() $(
  extrn read,ch,punch;
  auto a,v;
  punch(); leader(20); ch=read();
  while(ch!=004) $(
    if(ch=='i'|ch=='x'|ch=='w') $(
      ch=read(); a=getoct(); v=getoct(); record(a,v);
    $)
    while(ch!='*n'&ch!=004)ch=read();
    if(ch!=004)ch=read();
  $)
  transfer(1); leader(20);
$)
getoct() $(
  extrn read,ch; auto v;
  while(ch==' ')ch=read(); v=0;
  while(ch>='0'&ch<='7')$(v=v*8+ch-'0';ch=read();$)
  return(v);
$)
byte(v) $(
  extrn write,sum;
  v=v&0377; sum=(sum+v)&0377;
  if(v==0)v=0400;          /* defeat PDP-7 UNIX NUL suppression */
  write(v);
$)
record(a,v) $(
  extrn sum; sum=0;
  byte(1);byte(0);byte(8);byte(0);
  byte(a);byte(a/0400);byte(v);byte(v/0400);
  byte(-sum);
$)
transfer(a) $(
  extrn sum; sum=0;
  byte(1);byte(0);byte(6);byte(0);byte(a);byte(a/0400);byte(-sum);
$)
leader(n) $(
  extrn write; auto i; i=0;
  while(i<n)$(write(0400);i=i+1;$)
$)
sum;
ch;
