def fibonacci(n):
  fib_list = [0, 1]
  
  for i in range(n):
    temp = fib_list[0] + fib_list[1]
    fib_list[0] = fib_list[1]
    fib_list[1] = temp
  return fib_list[0]