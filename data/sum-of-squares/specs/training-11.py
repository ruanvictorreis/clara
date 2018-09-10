def sum_of_squares(n):
  soma = 0 
  i = 1
  while n >= i: 
    soma = soma + i**2
    i = i + 1
  return soma
