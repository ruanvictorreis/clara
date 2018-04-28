def factorial(n):
  total = 1
  for i in range(n):
    total = (n-1)*(n)*(total)
  return total
