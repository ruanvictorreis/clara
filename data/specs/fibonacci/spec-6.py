def fibonacci(n):
  a = 0
  b = 1
  while(n > 0):
    a, b = b, a+b
    n = n - 1
  return a
