add(a, b) $(
  return(a + b);
$)

main $(
  if (add(2, 3) == 5)
    write('G7');
  else
    write('F7');
$)
