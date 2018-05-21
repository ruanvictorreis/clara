def factorial(n):
  total = 1
  for i in range(n, 1, -1):
    total = total * i
  return total
