def is_prime_number(n):
  lista = []
  for i in range(1, n+1):
    if n % i == 0:
      lista.append(i) 
  
  if len(lista) == 2:
    return True
  else:
    return False
