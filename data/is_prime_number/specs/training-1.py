def is_prime_number(n):
  prime = True
  i = 2
  
  while i < n and prime:
    if n % i == 0:
      prime = False
    i += 1	
  return prime and n != 1
