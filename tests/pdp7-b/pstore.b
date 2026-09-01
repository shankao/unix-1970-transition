main $(
  auto a, b;
  a = 4;
  b = a;
  a = b + 2;
  if (a == 6 & b == 4)
    write('S2');
  else
    write('F2');
$)
