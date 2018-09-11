def fibonacci(n):
  if n == 0:
    return 0
    
  f_ant = 0
  f_atual = 1
  
  for i in range(n-1):
    f_prox = f_ant + f_atual
    f_ant = f_atual
    f_atual = f_prox	  
  return f_atual