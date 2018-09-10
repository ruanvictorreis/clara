def sum_of_squares(n):
  total = 0
  count = 1
  while count <= n:
    total = total + (count**2)
    count = count + 1
  return total
