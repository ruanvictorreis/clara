def fibonacci(n): 
  if n == 0:
    return 0
  
  if n == 1:
    return 1
    
  lista = [0, 1]
  
  for i in range(2, n+1):
    lista.append(lista[i-1] + lista[i-2])
  return lista[n]
