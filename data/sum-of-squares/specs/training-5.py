def sum_of_squares(n):
  total = 0
  for i in range(n, 0, -1):
    total = total + (i*i)
  return total
