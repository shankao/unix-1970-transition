/* Stage 4C as11 language, symbol, and KA11 encoding engine.
 * Class B reconstruction.  Trace output remains test instrumentation.
 */

main() $(
  extrn pass, line, loc, bad, nglob, nlocal, rewind, flush;
  bad = 0;
  nglob = 0;
  nlocal = 0;
  pass = 1;
  initrun();
  program();
  if (bad == 0) $(
    rewind();
    pass = 2;
    initrun();
    program();
    if (bad == 0) undefck();
  $)
  flush();
$)

initrun() $(
  extrn line, loc, bad, havec, pass, occ;
  auto i;
  line = 1;
  loc = 0;
  havec = 0;
  i = 0;
  while (i < 10) $(
    occ[i] = 0;
    i = i + 1;
  $)
$)

getch() $(
  extrn havec, pushc, read;
  auto c;
  if (havec) $(
    havec = 0;
    return(pushc);
  $)
  c = read();
  return(c);
$)

unget(c) $(
  extrn havec, pushc;
  havec = 1;
  pushc = c;
$)

next() $(
  extrn tok, tval, tdigit, tdir, line, tline, bad,tname,ctab;
  auto c, i, v, inv,p;
again:
  c = getch();
  if (c == 004) $( tok = 0; return; $)
  if (c == ' ' | c == '*t') goto again;
  if (c == '*n') $(
    tok = 1; tline = line; line = line + 1; return;
  $)
  if (c == ';') $( tok = 1; tline = line; return; $)
  if (c == '/') $(
    c = getch();
    while (c != '*n' & c != 004) c = getch();
    if (c == 004) $( tok = 0; return; $)
    tok = 1; tline = line; line = line + 1; return;
  $)
  tline = line;
  if ((c>='a'&c<='z')|(c>='A'&c<='Z')|c=='_') $(
    i=0;while(i<4)$(tname[i]=0;i=i+1;$)i=0;
    while ((c>='a'&c<='z')|(c>='A'&c<='Z')|c=='_'|(c>='0'&c<='9')) $(
      if(i<8)$(p=i/2;if((i%2)==0)tname[p]=c*512;
        else tname[p]=tname[p]+c;$)
      i = i + 1;
      c = getch();
    $)
    unget(c);
    tok = 2;
    return;
  $)
  if (c>='0'&c<='9') $(
    v = 0;
    inv = 0;
    while (c>='0'&c<='9') $(
      if (c > '7') inv = 1;
      v = v * 8 + c - '0';
      c = getch();
    $)
    if ((c == 'f' | c == 'b') & v < 10) $(
      tok=4;tdigit=v;tdir=c;return;
    $)
    if (c == ':' & v < 10) $(
      unget(c); tok = 3; tval = v; return;
    $)
    if (inv) $( tok = 99; return; $)
    unget(c);
    tok = 3; tval = v; return;
  $)
  i=0;while(i<12)$(if(c==ctab[i])$(tok=i+5;return;$)i=i+1;$)
  tok = 99;
$)

cpname(d,s) $(
  auto i;
  i = 0;
  while (i < 4) $( d[i] = s[i]; i = i + 1; $)
$)

gfind(name,make) $(
  extrn nglob;
  auto i, p;
  i = 0;
  while (i < nglob) $(
    p = 017537-i*5;
    if((p[0]&0177777)==name[0]&p[1]==name[1]&p[2]==name[2]&p[3]==name[3])return(p);
    i = i + 1;
  $)
  if (make == 0) return(0);
  if (nglob >= 48) $( fail('gf'); return(0); $)
  p = 017537-nglob*5;
  cpname(p,name);
  p[4] = 0;
  nglob = nglob + 1;
  return(p);
$)

resolve(name) $(
  extrn eres;
  auto p;
  p = gfind(name,1);
  if (p == 0 | (p[0]&0600000) == 0) $( eres = 0; return(0); $)
  eres = 1;
  return(p[4]);
$)

lfind(key) $(
  extrn nlocal;
  auto i,p;
  i = 0;
  while (i < nlocal) $(
    p=017544+i*2;if(p[0]==key)return(p);
    i = i + 1;
  $)
  return(0);
$)

localref(d,dir) $(
  extrn eres, occ;
  auto n, p;
  n = occ[d];
  if(dir=='f')n=n+1;
  if (n == 0) $( eres = 0; return(0); $)
  p = lfind(d*100+n);
  if (p == 0) $( eres = 0; return(0); $)
  eres = 1;
  return(p[1]);
$)

primary() $(
  extrn tok, tval, tdigit, tdir, loc, eres, bad, tname;
  auto v,nm 4;
  if (tok == 7) $(
    next();
    v = primary();
    return(-v);
  $)
  if (tok == 8) $(
    next();
    v = expr();
    if (tok != 9) $( fail('rb'); return(0); $)
    next();
    return(v);
  $)
  if (tok == 3) $( v = tval; eres = 1; next(); return(v); $)
  if (tok == 5) $( eres = 1; v = loc; next(); return(v); $)
  if(tok==4|tok==17) $(
    v=localref(tdigit,tdir);
    next();
    return(v);
  $)
  if (tok == 2) $(
    cpname(nm,tname);
    next();
    return(resolve(nm));
  $)
  fail('xp');
  return(0);
$)

expr() $(
  extrn eres; auto v,ok;
  v=primary();ok=eres;return(moreexpr(v,ok));
$)

endstmt() $(
  extrn tok;
  if (tok != 0 & tok != 1) fail('st');
$)

defglob(name) $(
  extrn pass, loc;
  auto p;
  p = gfind(name,1);
  if (p == 0) return;
  if (pass == 1) $(
    if ((p[0]&0600000) != 0) $( fail('gd'); return; $)
    p[0]=p[0]+0200000;p[4]=loc;
  $) else $(
    if ((p[0]&0600000)!=0200000|p[4]!=loc) $( fail('ph'); return; $)
    outname('l ',name,loc);
  $)
$)

setglob(name) $(
  extrn pass, eres, bad;
  auto p, v;
  v = expr();
  if (bad) return;
  if (eres == 0) $( fail('ur'); return; $)
  p = gfind(name,1);
  if (p == 0) return;
  if ((p[0]&0600000)==0200000) $( fail('ga'); return; $)
  p[0]=(p[0]&0177777)+0400000;p[4]=v;
  if (pass == 2) outname('a ',name,v);
$)

deflocal(d) $(
  extrn pass, nlocal, loc, occ,write;
  auto key, p;
  occ[d] = occ[d] + 1;
  key = d*100 + occ[d];
  if (pass == 1) $(
    if (nlocal >= 10) $( fail('lf'); return; $)
    p=017544+nlocal*2;p[0]=key;p[1]=loc;
    nlocal = nlocal + 1;
  $) else $(
    p = lfind(key);
    if (p == 0 | p[1] != loc) $( fail('ph'); return; $)
    write('n ');write(d+'0');write(' ');putoct6(loc);write('*n');
  $)
$)

rawword(v,ok) $(
  extrn loc,pass,bad;
  if(loc<0|loc>0177776)$(fail('ad');return;$)
  if(loc&1)$(fail('od');return;$)
  endstmt();if(bad)return;
  if(pass==2)$(if(ok==0)$(fail('un');return;$)
    if(v>=0&v>0177777)$(fail('wv');return;$)
    outcode('w ',loc,v&0177777);$)
  loc=loc+2;if(loc>0200000)fail('ov');
$)

statement() $(
  extrn tok, tval, loc, eres, pass, tname, bad;
  auto nm 4, v, d;
  if (tok == 2) $(
    cpname(nm,tname);
    next();
    if (tok == 10) $( next(); defglob(nm); endstmt(); return; $)
    if (tok == 11) $( next(); setglob(nm); endstmt(); return; $)
    if (mfind(nm)) $( instruction(); return; $)
    v = resolve(nm);
    exprtail(v,eres);
    return;
  $)
  if (tok == 3) $(
    d = tval;
    next();
    if (tok == 10) $(
      if (d > 9) $( fail('nl'); return; $)
      next(); deflocal(d); endstmt(); return;
    $)
    exprtail(d,1);
    return;
  $)
  if (tok == 5) $(
    next();
    if (tok == 11) $(
      next(); v = expr();
      if (bad) return;
      if (eres == 0) $( fail('ur'); return; $)
      if (v < 0 | v > 0177777) $( fail('ad'); return; $)
      loc = v; endstmt(); return;
    $)
    exprtail(loc,1);
    return;
  $)
  v=expr();if(bad)return;rawword(v,eres);
$)

/* Table order supplies the compact encoding class. */
mfind(n) $(
  extrn mclass,mop,mtab; auto i,p;
  if(n[2]!=0|n[3]!=0)return(0);
  i=0;
  while(i<21) $(
    p=mtab+i*3;
    if(n[0]==p[0]&n[1]==p[1]) $(
      mclass=i+1;mop=p[2];return(1);
    $)
    i=i+1;
  $)
  mclass=0;return(0);
$)

regno(n) $(
  if(n[1]!=0|n[2]!=0|n[3]!=0)return(-1);
  if(n[0]>='r0'&n[0]<='r5')return(n[0]-'r0');
  if(n[0]=='sp')return(6); if(n[0]=='pc')return(7); return(-1);
$)

getreg() $(
  extrn tok,tname; auto r;
  if(tok!=2)$(fail('rg');return(0);$)
  r=regno(tname); if(r<0)$(fail('rg');return(0);$) next(); return(r);
$)

parreg() $(
  extrn tok;auto r;
  if(tok!=12)$(fail('ea');return(0);$)
  next();r=getreg();if(tok!=13)$(fail('rp');return(0);$)next();return(r);
$)

moreexpr(v,ok) $(
  extrn tok,eres,bad; auto r,op;
  while(bad==0&(tok==6|tok==7)) $(
    op=tok;next();r=primary();if(eres==0)ok=0;
    if(op==6)v=v+r;else v=v-r;
  $)
  eres=ok;return(v);
$)

/* oe is 0/absolute-extension/relative-extension; ov is its value. */
operand() $(
  extrn tok,tname,oe,ov,eres,bad,pass;
  auto star,r,v;
  oe=0;ov=0;star=0;
  if(tok==16)$(star=1;next();$)
  if(tok==15)$(next();v=expr();if(pass==2&eres==0)$(fail('un');return(0);$)
    oe=1;ov=v;
    if(star)return(037);return(027);$)
  if(tok==12)$(r=parreg();if(tok==6)$(next();if(star)return(030+r);return(020+r);$)
    if(star)$(fail('ea');return(0);$) return(010+r);$)
  if(tok==7)$(next();if(tok==12)$(r=parreg();
      if(star)return(050+r);return(040+r);$)
    v=-primary();v=moreexpr(v,eres);$)
  else if(tok==2)$(r=regno(tname);
    if(r>=0)$(next();if(star)$(fail('ea');return(0);$)return(r);$)
    v=expr();$)
  else v=expr();
  if(bad)return(0);if(pass==2&eres==0)$(fail('un');return(0);$)
  if(tok==12)$(r=parreg();oe=1;ov=v;
    if(star)return(070+r);return(060+r);$)
  oe=2;ov=v;if(star)return(077);return(067);
$)

outcode(k,a,v) $(extrn write;write(k);putoct6(a);write(' ');putoct6(v);write('*n');$)

emitext(v,r,a) $(
  extrn bad;
  if(r)$(if(v<0|v>0177777)$(fail('ad');return;$)v=v-a-2;$)
  else if(v>=0&v>0177777)$(fail('wv');return;$)
  if(bad==0)outcode('x ',a,v&0177777);
$)

finishins(w) $(
  extrn loc,pass,bad,se,sv,de,dv;
  auto a,e,n;a=loc;n=1+(se!=0)+(de!=0);
  if(a&1)$(fail('ad');return;$)
  if(a+2*n>0200000)$(fail('ov');return;$)
  if(pass==2)$(
    outcode('i ',a,w&0177777);e=a+2;
    if(se)$(emitext(sv,se==2,e);if(bad)return;e=e+2;$)
    if(de)emitext(dv,de==2,e);
  $)
  loc=a+2*n;
$)

instruction() $(
  extrn mclass,mop,tok,pass,loc,eres,bad,oe,ov;
  extrn se,sv,de,dv;
  auto s,d,v,delta,r;
  se=0;de=0;
  if(mclass==1|mclass==17)$(endstmt();if(bad)return;
    finishins(mop);return;$)
  if(mclass==21)$(v=expr();r=eres;endstmt();if(bad)return;
    if(pass==2)$(if(r==0)$(fail('un');return;$)
      if(v<0|v>0377)$(fail('tv');return;$)$)
    finishins(mop+(v&0377));return;$)
  if(mclass>=11&mclass<=13)$(v=expr();r=eres;endstmt();if(bad)return;
    if(loc&1)$(fail('ad');return;$)
    if(pass==2)$(if(r==0)$(fail('un');return;$)
      if(v<0|v>0177777|(v&1))$(fail('br');return;$)
      delta=v-loc-2;if(delta < -0400)$(fail('br');return;$)
      if(delta > 0376)$(fail('br');return;$)
      if(delta<0)delta=-((-delta)/2);else delta=delta/2;
      outcode('i ',loc,mop+(delta&0377));$) loc=loc+2;return;$)
  if(mclass==16)$(r=getreg();endstmt();if(bad)return;
    finishins(mop+r);return;$)
  if(mclass==15)$(r=getreg();if(tok!=14)$(fail('cm');return;$)
    next();d=operand();de=oe;dv=ov;endstmt();if(bad)return;
    if((d/8)==0)$(fail('jm');return;$)
    finishins(mop+r*64+d);return;$)
  s=operand();se=oe;sv=ov;
  if((mclass>=2&mclass<=6)|mclass==14)$(endstmt();if(bad)return;
    if(mclass==14&(s/8)==0)$(fail('jm');return;$)
    finishins(mop+s);return;$)
  if(tok!=14)$(fail('cm');return;$)
  next();d=operand();de=oe;dv=ov;endstmt();if(bad)return;
  finishins(mop+s*64+d);
$)

exprtail(v,ok) $(
  extrn eres;v=moreexpr(v,ok);rawword(v,eres);
$)

program() $(
  extrn tok, bad;
  next();
  while (tok != 0 & bad == 0) $(
    if (tok == 1) next();
    else statement();
  $)
$)

undefck() $(
  extrn nglob,bad;
  auto i, p;
  i = 0;
  while (i < nglob & bad == 0) $(
    p=017537-i*5;
    if ((p[0]&0600000)==0) fail('un');
    i = i + 1;
  $)
$)

fail(code) $(
  extrn bad, tline, write;
  if (bad) return;
  bad = 1;
  write('e '); putoct6(tline); write(' '); write(code); write('*n');
$)

putoct6(v) $(
  extrn write;
  auto d, i;
  v = v & 0177777;
  d = 0100000; i = 0;
  while (i < 6) $(
    write((v/d)%8+'0');
    d = d/8; i = i+1;
  $)
$)

outname(k,n,v) $(
  extrn write;auto i;
  write(k);write(n[0]&0177777);i=1;
  while(i<4)$(if(n[i]==0)goto done;write(n[i]);i=i+1;$)
done: write(' ');putoct6(v);write('*n');
$)

occ[10];
tname[4];
nglob;
nlocal;
pass;
line;
loc;
bad;
havec;
pushc;
tok;
tval;
tdigit;
tdir;
tline;
eres;
mclass;
mop;
oe;
ov;
se;sv;
de;dv;
mtab[63]
  0150141,0154164,000000,
  0143154,0162000,005000,
  0164163,0164000,005700,
  0164163,0164142,0105700,
  0141163,0154000,006300,
  0141163,0162000,006200,
  0155157,0166000,0010000,
  0155157,0166142,0110000,
  0143155,0160000,0020000,
  0141144,0144000,0060000,
  0142162,0000000,000400,
  0142156,0145000,001000,
  0142160,0154000,0100000,
  0152155,0160000,000100,
  0152163,0162000,004000,
  0162164,0163000,000200,
  0162164,0151000,000002,
  0142151,0164000,0030000,
  0142151,0143000,0040000,
  0142151,0163000,0050000,
  0164162,0141160,0104400;
ctab[12] '.','+','-','[',']',':','=','(',')',',','$','**';
