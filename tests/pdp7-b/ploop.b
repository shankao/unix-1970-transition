main $(
  auto i, sum;
  i = 0;
  sum = 0;
  while (i < 4) $(
    sum = sum + i;
    i = i + 1;
  $)
  if (sum == 6)
    write('L5');
  else
    write('F5');
$)
