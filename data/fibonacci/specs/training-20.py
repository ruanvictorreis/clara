def fibonacci(n):
  if n == 0:
    return 0
  
  if n == 1:
    return 1
    
  fib_list = [0, 1]
  count = 0
  
  while (count < n):
    atual = fib_list[len(fib_list) - 1]
    anterior = fib_list[len(fib_list) - 2]
    fib_list.append(atual + anterior)
    count = count + 1
  return fib_list[n]