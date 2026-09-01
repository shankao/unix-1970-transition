main $(
  auto a, b, c, d, e;
  a = 7 + 5;
  b = 9 - 4;
  c = 3 * 4;
  d = 13 / 3;
  e = 13 % 3;
  if (a == 12 & b == 5 & c == 12 & d == 4 & e == 1)
    write('A3');
  else
    write('F3');
$)
