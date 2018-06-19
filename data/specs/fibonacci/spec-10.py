def fibonacci(n):
  a = 0
  b = 1
  count = 0
  while(count < n):
    a, b = b, a+b
    n = n - 1
  return a
