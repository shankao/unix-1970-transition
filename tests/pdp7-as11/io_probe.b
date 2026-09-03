/* Stage 4A: PDP-7 B buffered-input restart and textual-octal probe. */

copy(n) $(
  extrn read, write;
  auto i;
  i = 0;
  while (i < n) $(
    write(read());
    i = i + 1;
  $)
$)

putoct6(v) $(
  extrn write;
  auto i, d;
  d = 0100000;
  i = 0;
  while (i < 6) $(
    write((v / d) % 8 + '0');
    d = d / 8;
    i = i + 1;
  $)
  write('*n');
$)

main $(
  extrn read, write, flush, rewind;
  auto ch, n;

  write('A1'); write('*n'); copy(17); write('*n');
  rewind();
  write('A2'); write('*n'); copy(17); write('*n');

  rewind();
  write('B1'); write('*n'); copy(173); write('*n');
  rewind();
  write('B2'); write('*n'); copy(173); write('*n');

  rewind();
  n = 0;
  ch = read();
  while (ch != 004) $(
    n = n + 1;
    ch = read();
  $)
  write('CE'); write('*n');
  putoct6(ch);
  putoct6(n);
  rewind();
  write('CR'); write('*n'); copy(17); write('*n');

  write('O:'); write('*n');
  putoct6(0);
  putoct6(1);
  putoct6(077777);
  putoct6(0100000);
  putoct6(0177777);
  flush();
$)
