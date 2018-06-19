def fibonacci(n):
  fib_list = [0, 1]
  count = 0
  while(count < n):
    size = len(fib_list)
    a = fib_list[size - 1]
    b = fib_list[size - 2]
    fib_list.append(a + b)
    count = count + 1
  return fib_list[n]
