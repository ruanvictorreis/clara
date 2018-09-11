def fibonacci(n):
  if n == 0:
    return 0
  
  if n == 1:
    return 1

  f_ant = 0
  f_atual = 1
  i = 1    
  
  while i < n:
    f_prox = f_ant + f_atual
    f_ant = f_atual
    f_atual = f_prox
    i = i + 1     
  return f_atual