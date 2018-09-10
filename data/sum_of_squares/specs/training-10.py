def sum_of_squares(n):
  total = 0
  number_list = range(1, n+1)
  for i in number_list:
    total = total + (i**2)
  return total
