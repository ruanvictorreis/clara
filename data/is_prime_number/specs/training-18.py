def is_prime_number(n):
  isPrime = True 
  count = 2 
  
  if n == 1:
    return False
  
  while (isPrime and count < n):
    if (n % count == 0): 
      isPrime = False 
    count += 1 
  return isPrime
