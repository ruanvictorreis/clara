def factorial(n):
  total = 1
  for i in range(n, 2, -1):
    total = total * (i - 1)
  return total * n
