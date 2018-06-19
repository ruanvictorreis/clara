def fibonacci(n):
  fib_list = [0, 1]
  count = n
  while(count > 0):
    a = fib_list[len(fib_list) - 1]
    b = fib_list[len(fib_list) - 2]
    fib_list.append(a + b)
    count = count - 1
  return fib_list[n]
