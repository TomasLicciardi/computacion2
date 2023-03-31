import argparse
import sys

def main():
    # Primero creamos un objeto de la clase ArgumenParser
    parser = argparse.ArgumentParser(description='Obtener lista de numeros impares con un numero entero positivo')
    
    # Luego establecemos que valor le vamos a pasar en línea de comandos con el tipo
    parser.add_argument('n', type=int, help='Numeros para la lista')
    #parse_args se utiliza para modo de verificar o de conversor del valor que le pasamos como argumento al tipo que nosotros queremos pasarlo
    args = parser.parse_args()

    # Vamos a establecer que dicho numero tiene que ser positivo
    if args.n <= 0:
        print("El número de elementos debe ser un entero positivo.")
        exit()

    # Genero la lista de los números impares 
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
