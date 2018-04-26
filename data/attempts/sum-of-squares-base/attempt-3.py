def sum_of_squares_base(base, n):
  sumn = 0
  for i in range(n,1,-1):
    sumn = i*i+sumn
  return (base+sumn)
