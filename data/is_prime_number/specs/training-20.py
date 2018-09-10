def is_prime_number(n):
  if n == 1:
    return False
  
  for x in range(2, n):
    if x == 1:
      break 
    elif n % x == 0:
      return False  
  return True
