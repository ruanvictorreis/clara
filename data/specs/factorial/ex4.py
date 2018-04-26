def factorial(n):
  produto = 1
  for i in range(n,1,-1):
    produto = produto * i
  return(produto)