def sum_of_squares_base(base, n):
	sumn = 0
	for a in range(n,1,-1):
		sumn = a*a + sumn
	return(base + sumn + 1)
