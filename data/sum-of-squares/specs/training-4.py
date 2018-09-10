def sum_of_squares(n):
  total = 0 
  for i in range(n):
    total = total + ((i+1) ** 2)
  return total
