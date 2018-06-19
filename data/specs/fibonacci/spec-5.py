def fibonacci(n):
  a = 0
  b = 1
  while(n > 0):
    c = a
    a = b
    b = c + b
    n = n - 1
  return a
