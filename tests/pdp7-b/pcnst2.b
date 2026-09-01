main $(
  auto a, b, c, ok;
  a = 7;
  b = -3;
  c = 020000;
  ok = 0;
  if (a == 7) ok = ok + 1;
  if (b == -3) ok = ok + 1;
  if (c == 020000) ok = ok + 1;
  if (ok == 3)
    write('C1');
  else
    write('F1');
$)
