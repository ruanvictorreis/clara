def is_prime_number(n):  
  for i in range(2, n):
    if n % i == 0:
      return False
  return True and n != 1
