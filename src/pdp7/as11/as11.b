/* Stage 4B as11 language and symbol engine.
 * Class B reconstruction.  No PDP-11 instruction encoding is present.
 */

main() $(
  extrn pass, line, loc, bad, nglob, nlocal, eof, rewind, flush;
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
  extrn line, loc, bad, eof, havec, pass, occ;
  auto i;
  line = 1;
  loc = 0;
  eof = 0;
  havec = 0;
  i = 0;
  while (i < 10) $(
    occ[i] = 0;
    i = i + 1;
  $)
$)

isalpha(c) $(
  if (c >= 'a' & c <= 'z') return(1);
  if (c >= 'A' & c <= 'Z') return(1);
  if (c == '_') return(1);
  return(0);
$)

isdigit(c) $(
  if (c >= '0' & c <= '9') return(1);
  return(0);
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

clrname() $(
  extrn tname;
  auto i;
  i = 0;
  while (i < 4) $(
    tname[i] = 0;
    i = i + 1;
  $)
$)

namechar(i,c) $(
  extrn tname;
  auto p;
  if (i >= 8) return;
  p = i / 2;
  if ((i % 2) == 0)
    tname[p] = c * 512;
  else
    tname[p] = tname[p] + c;
$)

next() $(
  extrn tok, tval, tdigit, tdir, line, tline, eof, bad;
  auto c, i, v, inv;
again:
  c = getch();
  if (c == 004) $( eof = 1; tok = 0; return; $)
  if (c == ' ' | c == '*t') goto again;
  if (c == '*n') $(
    tok = 1; tline = line; line = line + 1; return;
  $)
  if (c == ';') $( tok = 1; tline = line; return; $)
  if (c == '/') $(
    c = getch();
    while (c != '*n' & c != 004) c = getch();
    if (c == 004) $( eof = 1; tok = 0; return; $)
    tok = 1; tline = line; line = line + 1; return;
  $)
  tline = line;
  if (isalpha(c)) $(
    clrname();
    i = 0;
    while (isalpha(c) | isdigit(c)) $(
      namechar(i,c);
      i = i + 1;
      c = getch();
    $)
    unget(c);
    tok = 2;
    return;
  $)
  if (isdigit(c)) $(
    v = 0;
    inv = 0;
    while (isdigit(c)) $(
      if (c > '7') inv = 1;
      v = v * 8 + c - '0';
      c = getch();
    $)
    if ((c == 'f' | c == 'b') & v < 10) $(
      tok = 4; tdigit = v; tdir = c; return;
    $)
    if (c == ':' & v < 10) $(
      unget(c); tok = 3; tval = v; return;
    $)
    if (inv) $( tok = 99; return; $)
    unget(c);
    tok = 3; tval = v; return;
  $)
  if (c == '.') $( tok = 5; return; $)
  if (c == '+') $( tok = 6; return; $)
  if (c == '-') $( tok = 7; return; $)
  if (c == '[') $( tok = 8; return; $)
  if (c == ']') $( tok = 9; return; $)
  if (c == ':') $( tok = 10; return; $)
  if (c == '=') $( tok = 11; return; $)
  tok = 99;
$)

cpname(d,s) $(
  auto i;
  i = 0;
  while (i < 4) $( d[i] = s[i]; i = i + 1; $)
$)

same(a,b) $(
  auto i;
  i = 0;
  while (i < 4) $(
    if (a[i] != b[i]) return(0);
    i = i + 1;
  $)
  return(1);
$)

gfind(name,make) $(
  extrn nglob, gtab;
  auto i, p;
  i = 0;
  while (i < nglob) $(
    p = gtab + i * 6;
    if (same(p,name)) return(p);
    i = i + 1;
  $)
  if (make == 0) return(0);
  if (nglob >= 64) $( fail('gf'); return(0); $)
  p = gtab + nglob * 6;
  cpname(p,name);
  p[4] = 0;
  p[5] = 0;
  nglob = nglob + 1;
  return(p);
$)

resolve(name) $(
  extrn eres;
  auto p;
  p = gfind(name,1);
  if (p == 0 | p[4] == 0) $( eres = 0; return(0); $)
  eres = 1;
  return(p[5]);
$)

lfind(key) $(
  extrn nlocal, ltab;
  auto i;
  i = 0;
  while (i < nlocal) $(
    if (ltab[i*2] == key) return(ltab + i*2);
    i = i + 1;
  $)
  return(0);
$)

localref(d,dir) $(
  extrn eres, occ;
  auto n, p;
  n = occ[d];
  if (dir == 'f') n = n + 1;
  if (n == 0) $( eres = 0; return(0); $)
  p = lfind(d*100+n);
  if (p == 0) $( eres = 0; return(0); $)
  eres = 1;
  return(p[1]);
$)

primary() $(
  extrn tok, tval, tdigit, tdir, loc, eres, bad, tname;
  auto v, r, nm 4;
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
  if (tok == 4) $(
    v = localref(tdigit,tdir);
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
  extrn tok, eres, bad;
  auto v, r, ok, op;
  v = primary();
  ok = eres;
  while (bad == 0 & (tok == 6 | tok == 7)) $(
    op = tok;
    next();
    r = primary();
    if (eres == 0) ok = 0;
    if (op == 6) v = v + r;
    else v = v - r;
  $)
  eres = ok;
  return(v);
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
    if (p[4] != 0) $( fail('gd'); return; $)
    p[4] = 1; p[5] = loc;
  $) else $(
    if (p[4] != 1 | p[5] != loc) $( fail('ph'); return; $)
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
  if (p[4] == 1) $( fail('ga'); return; $)
  p[4] = 2; p[5] = v;
  if (pass == 2) outname('a ',name,v);
$)

deflocal(d) $(
  extrn pass, nlocal, loc, occ, ltab;
  auto key, p;
  occ[d] = occ[d] + 1;
  key = d*100 + occ[d];
  if (pass == 1) $(
    if (nlocal >= 64) $( fail('lf'); return; $)
    ltab[nlocal*2] = key;
    ltab[nlocal*2+1] = loc;
    nlocal = nlocal + 1;
  $) else $(
    p = lfind(key);
    if (p == 0 | p[1] != loc) $( fail('ph'); return; $)
    outlocal(d,loc);
  $)
$)

wordexpr() $(
  extrn loc, pass, eres, bad;
  auto v;
  if (loc < 0 | loc > 0177776) $( fail('ad'); return; $)
  if (loc & 1) $( fail('od'); return; $)
  v = expr();
  if (bad) return;
  endstmt();
  if (bad) return;
  if (pass == 2) $(
    if (eres == 0) $( fail('un'); return; $)
    if (v >= 0 & v > 0177777) $( fail('wv'); return; $)
    outword(loc,v & 0177777);
  $)
  loc = loc + 2;
  if (loc > 0200000) fail('ov');
$)

statement() $(
  extrn tok, tval, loc, eres, pass, tname, bad;
  auto nm 4, v, d;
  if (tok == 2) $(
    cpname(nm,tname);
    next();
    if (tok == 10) $( next(); defglob(nm); endstmt(); return; $)
    if (tok == 11) $( next(); setglob(nm); endstmt(); return; $)
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
  wordexpr();
$)

exprtail(v,ok) $(
  extrn tok, eres, loc, pass, bad;
  auto r, op;
  if (loc < 0 | loc > 0177776) $( fail('ad'); return; $)
  if (loc & 1) $( fail('od'); return; $)
  while (bad == 0 & (tok == 6 | tok == 7)) $(
    op = tok; next(); r = primary();
    if (eres == 0) ok = 0;
    if (op == 6) v = v + r; else v = v - r;
  $)
  endstmt();
  if (bad) return;
  if (pass == 2) $(
    if (ok == 0) $( fail('un'); return; $)
    if (v >= 0 & v > 0177777) $( fail('wv'); return; $)
    outword(loc,v & 0177777);
  $)
  loc = loc + 2;
  if (loc > 0200000) fail('ov');
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
  extrn nglob, gtab, bad;
  auto i, p;
  i = 0;
  while (i < nglob & bad == 0) $(
    p = gtab + i*6;
    if (p[4] == 0) fail('un');
    i = i + 1;
  $)
$)

fail(code) $(
  extrn bad, tline, tok, eof, write;
  auto c;
  if (bad) return;
  bad = 1;
  write('e '); putoct6(tline); write(' '); write(code); write('*n');
  c = getch();
  while (c != 004) c = getch();
  eof = 1; tok = 0;
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

printname(n) $(
  extrn write;
  auto i, c, w;
  i = 0;
  while (i < 8) $(
    w = n[i/2];
    if ((i%2)==0) c = (w/512)&0777;
    else c = w&0777;
    if (c == 0) return;
    write(c); i = i+1;
  $)
$)

outname(k,n,v) $(
  extrn write;
  write(k); printname(n); write(' '); putoct6(v); write('*n');
$)

outlocal(d,v) $(
  extrn write;
  write('n '); write(d+'0'); write(' '); putoct6(v); write('*n');
$)

outword(a,v) $(
  extrn write;
  write('w '); putoct6(a); write(' '); putoct6(v); write('*n');
$)

gtab[384];
ltab[128];
occ[10];
tname[4];
nglob;
nlocal;
pass;
line;
loc;
bad;
eof;
havec;
pushc;
tok;
tval;
tdigit;
tdir;
tline;
eres;
