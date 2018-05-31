def factorial(n):
  total = 0
  count = 0
  while count >= n:
    total = count * count
    count = count + 1
  return total
