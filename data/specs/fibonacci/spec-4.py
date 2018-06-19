def fibonacci(n):
  fib_list = [0, 1]
  for i in range(n):
    size = len(fib_list)
    a = fib_list[size - 1]
    b = fib_list[size - 2]
    fib_list.append(a + b)
  return fib_list[n]
