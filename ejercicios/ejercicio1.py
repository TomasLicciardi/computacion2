import argparse
import sys

def main():

    parser = argparse.ArgumentParser(description='Obtener lista de numeros impares con un numero entero positivo')
    
    parser.add_argument('n', type=int, help='Numeros para la lista')
    
    args = parser.parse_args()

    if args.n <= 0:
        print("El número de elementos debe ser un entero positivo.")
        exit()

    impares = []
    n_impares = 0
    i = 1
    while n_impares < args.n:
        impares.append(i)
        n_impares += 1
        i += 2

    print(impares)

if __name__ == '__main__':
    main()
