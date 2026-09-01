main $(
  auto v 3;
  v[0] = 2;
  v[1] = 3;
  if (v[0] + v[1] == 5)
    write('V8');
  else
    write('F8');
$)
