def sum_of_squares(n):
  quad = [i**2 for i in range(1, n+1)]
  soma = 0 
  for i in quad:
    soma += i
  return soma
