def fibonacci(n):
  fib_list = []
  for i in range(n):
    s = len(fib_list)
    a = fib_list[size - 1]
    b = fib_list[size - 2]
    fib_list.append(b)  
  return fib_list[n - 1]
