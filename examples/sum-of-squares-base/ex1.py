def sum_of_squares_base(base, n):
  contador = base
  for i in range(n+1):
    contador = contador + i**2
  return contador
