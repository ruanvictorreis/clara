def sum_of_squares_base(base, n):
  total = 0
  for i in range(n,1,-1):
    total = i*i+total
  return total