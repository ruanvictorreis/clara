def fibonacci(n): 
  lista = [0, 1]
  
  for i in range(2, n+1):
    lista.append(lista[i-1] + lista[i-2])
  return lista[n]
