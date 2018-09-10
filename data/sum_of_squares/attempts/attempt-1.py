def sum_of_squares(n):
  soma = 0
  for i in range(1, n+1):
    soma = soma + (i ** 2)
  return soma
