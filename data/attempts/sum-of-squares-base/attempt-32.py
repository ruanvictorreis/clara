def sum_of_squares_base(base, n):
  total = base
  for i in range(n):
	total = base + n**2
  return total
