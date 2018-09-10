def is_prime_number(n):
  if n == 1:
    return False
  
  isPrime = True
  for i in range(2, n):
    if n % i == 0:
      isPrime = False
  return isPrime
