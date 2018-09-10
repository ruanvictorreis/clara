def is_prime_number(n):
  if n == 1:
    return False
  
  for x in range(n-1, 0, -1):
    if x == 1:
      break
    elif n % x == 0:
      return False
  return True
