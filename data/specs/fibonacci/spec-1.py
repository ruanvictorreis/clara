def fibonacci(n):
  a = 0
  b = 1
  for i in range(n):
    c = a
    a = b
    b = c + b
  return a
