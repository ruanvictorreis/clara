def is_prime_number(n):
  if n == 1:
    return False 
  
  if n <= 3:
    return True
  
  for i in range(2, n, 1):
    if n % i == 0:
      return False
  return True
