def sum_of_squares(n):
  num = 0
  while n >= 1:
    num = num + (n*n)
    n = n - 1
  return num
