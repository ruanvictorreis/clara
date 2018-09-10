def sum_of_squares(n): 
  soma = 0
  i = 1 
  for x in range(n):
    soma = soma + i**2
    i = i + 1 
  return soma
