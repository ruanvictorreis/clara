def fibonacci(n):
  value = 0
  values = [0, 1]
  for i in range(n):
    value = values[0] + values[1]
    values[0] = values[1]
    values[1] = value
  return values[0]
