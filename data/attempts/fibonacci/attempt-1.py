def fibonacci(n):
  anterior = 0
  proximo = 1
  i = 0
  while i <= (n - 1):
    anterior = proximo
    proximo = anterior + proximo
    n = n - 1  
  return anterior
