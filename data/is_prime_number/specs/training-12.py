def is_prime_number(n):
  isPrime = True
  for i in range(2, n):
    if n % i == 0:
      isPrime = False
  return isPrime and n != 1
