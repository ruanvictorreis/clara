def is_prime_number(n):
  count = 0
  for i in range(1, n+1):
    if n % i == 0:
      count += 1 
  
  if count == 2:
    return True
  else:
    return False
