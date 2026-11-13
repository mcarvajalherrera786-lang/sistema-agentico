def fibonacci(n):
    """Calcula los primeros n términos de la serie de Fibonacci."""
    serie = []
    a, b = 0, 1
    for _ in range(n):
        serie.append(a)
        a, b = b, a + b
    return serie


if __name__ == "__main__":
    n = 10
    resultado = fibonacci(n)
    print(f"Serie de Fibonacci hasta el término {n}:")
    print(resultado)
