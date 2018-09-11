def fibonacci(n):
  if n == 0:
    return 0
  
  if n == 1:
    return 1

  fib_list = [0, 1]
  
  for i in range(n):
    temp = fib_list[0] + fib_list[1]
    fib_list[0] = fib_list[1]
    fib_list[1] = temp
  return fib_list[0]