main $(
  auto v 3, p;
  v[0] = 2;
  v[1] = 3;
  p = &v[1];
  *p = 4;
  if (v[0] + v[1] == 6)
    write('V8');
  else
    write('F8');
$)
