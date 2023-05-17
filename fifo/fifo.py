'''Escribir un programa que realice la multiplicación de dos matrices de 2x2. Cada elemento deberá calcularse en un proceso distinto devolviendo el resultado en una fifo indicando el indice del elemento. El padre deberá leer en la fifo y mostrar el resultado final.'''
import argparse
import multiprocessing
import os

def multiplicar_matrices(matriza,matrizb,proceso):
    if proceso == 1:
        elemento = matriza[0][0] * matrizb[0][0] + matriza[0][1] * matrizb[1][0]
    elif proceso == 2:
        elemento = matriza[0][0] * matrizb[0][1] + matriza[0][1] * matrizb[1][1]
    elif proceso == 3:
        elemento = matriza[1][0] * matrizb[0][0] + matriza[1][1] * matrizb[1][0]
    else:
        elemento = matriza[1][0] * matrizb[0][1] + matriza[1][1] * matrizb[1][1]

    with open('fifo', 'a') as fifo:
        fifo.write(f'{proceso},{elemento}\n')


def main():
    parser = argparse.ArgumentParser(description='Multiplicación de matrices de 2x2')
    parser.add_argument('a1', type=int, help='Elemento a1 de la matriz A')
    parser.add_argument('a2', type=int, help='Elemento a2 de la matriz A')
    parser.add_argument('a3', type=int, help='Elemento a3 de la matriz A')
    parser.add_argument('a4', type=int, help='Elemento a4 de la matriz A')
    parser.add_argument('b1', type=int, help='Elemento b1 de la matriz B')
    parser.add_argument('b2', type=int, help='Elemento b2 de la matriz B')
    parser.add_argument('b3', type=int, help='Elemento b3 de la matriz B')
    parser.add_argument('b4', type=int, help='Elemento b4 de la matriz B')
    args = parser.parse_args()

    matriza = [[args.a1, args.a2],
            [args.a3, args.a4]]
    matrizb = [[args.b1, args.b2],
                [args.b3, args.b4]]

    nombre_fifo = 'fifo'

    if os.path.exists(nombre_fifo):
        os.mkfifo(nombre_fifo)
    
    procesos = []
    for i in range(1,5):
        proceso = multiprocessing.Process(target=multiplicar_matrices,args=(matriza,matrizb,i))
        procesos.append(proceso)
        proceso.start()

    for procesos in procesos:
        print(proceso)
        proceso.join()
    
    resultados = {}
    with open(nombre_fifo, 'r') as fifo:
        for linea in fifo:
            proceso, resultado = linea.strip().split(',')
            resultados[int(proceso)] = int(resultado)

    print('Resultado final:')
    for i in range(1, 5):
        print(f'Proceso {i}: {resultados[i]}')

    os.remove(nombre_fifo)

if __name__ == '__main__':
    main()