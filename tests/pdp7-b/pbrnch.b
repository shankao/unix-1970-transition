main $(
  auto ok;
  ok = 0;
  if (2 < 3)
    ok = ok + 1;
  if (3 <= 3)
    ok = ok + 1;
  if (4 > 3)
    ok = ok + 1;
  if (4 >= 4)
    ok = ok + 1;
  if (4 != 5)
    ok = ok + 1;
  if (5 == 5)
    ok = ok + 1;
  if (ok == 6)
    write('B4');
  else
    write('F4');
$)
