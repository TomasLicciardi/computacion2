import concurrent.futures

def es_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def buscar_primo_inferior(valor):
    for i in range(valor - 1, 1, -1):
        if es_primo(i):
            return i

if __name__ == "__main__":
    valor_dado = int(input("Ingresar valor: "))
    
    max_procesos_concurrentes = 5

    with concurrent.futures.ProcessPoolExecutor(max_procesos_concurrentes) as executor:
        resultados = [executor.submit(buscar_primo_inferior, valor_dado - i) for i in range(max_procesos_concurrentes)]

        for resultado in concurrent.futures.as_completed(resultados):
            primo_inferior = resultado.result()
            if primo_inferior:
                print(f"El número primo inmediatamente inferior a {valor_dado} es {primo_inferior}")
                break
