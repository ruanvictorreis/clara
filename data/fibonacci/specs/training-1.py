def fibonacci(n):
  atual = 0
  proximo = 1
  
  for i in range(n):
    temp = atual
    atual = proximo
    proximo = temp + proximo
  return atual