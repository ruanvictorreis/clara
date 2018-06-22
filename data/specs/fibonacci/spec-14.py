def fibonacci(n):
  value = 0
  values = [0, 1]
  
  if n == 0:
    return value
  
  if n == 1:
    return values[0] + values[1]
  
  for i in range(1, n):
    value = values[0] + values[1]
    values[0] = values[1]
    values[1] = value 
  return value

for i in range(10):
	print(fibonacci(i))
