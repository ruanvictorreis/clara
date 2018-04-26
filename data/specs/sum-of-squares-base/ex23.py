def sum_of_squares_base(base, n):
    soma = base
    for i in range(n):
        soma = soma + ((i+1)**2)
    return (soma)

