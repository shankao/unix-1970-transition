main $(
  auto a, b, c, d, e, ok;
  a = 7 + 5;
  b = 9 - 4;
  c = 3 * 4;
  d = 13 / 3;
  e = 13 % 3;
  ok = 0;
  if (a == 12) ok = ok + 1;
  if (b == 5) ok = ok + 1;
  if (c == 12) ok = ok + 1;
  if (d == 4) ok = ok + 1;
  if (e == 1) ok = ok + 1;
  if (ok == 5)
    write('A3');
  else
    write('F3');
$)
