def fibonacci(n):
  a = 0
  b = 1
  count = 0
  while(count < n):
    c = a
    a = b
    b = c + b
    n = n - 1
  return a
