def sum_of_squares_base(base, n):
  total = base
  for i in range(n):
    total = base + (i^2)
    
sum_of_squares_base(5,3)    		
