def is_prime_number(n):
  if n == 1:
    return False

  prime = True
  i = 2 
  
  while i < n and prime:
    if n % i == 0:
      prime = False
    i += 1	
  return prime
