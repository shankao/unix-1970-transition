main $(
  auto x, p;
  x = 3;
  p = &x;
  *p = 4;
  if (x == 4)
    write('I8');
  else
    write('F8');
$)
