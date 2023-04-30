'''
Escribir un programa en Python que comunique dos procesos. El proceso padre deberá leer un archivo de texto y enviar cada línea del archivo al proceso hijo a través de un pipe. El proceso hijo deberá recibir las líneas del archivo y, por cada una de ellas, contar la cantidad de palabras que contiene y mostrar ese número.
'''
import multiprocessing
import argparse
import os

def recibir_informacion(conexion):
    while True:
        linea = conexion.recv()
        if linea == 'fin':
            break
        contar_palabras = linea.strip().split()
        if len(contar_palabras) == 0:
            continue
        print(f'Se recibio la linea y tiene {len(contar_palabras)} palabras')
        print(f'El proceso hijo {os.getpid()} recibio la informacion')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Proceso padre lee un archivo de texto y envia cada linea al proceso hijo a traves de un pipe. El proceso hijo recibe las lineas y cuenta la cantidad de palabras que contiene')
    parser.add_argument('-a','--archivo',type=str, help='Aca se va a pasar el archivo que vamos a leer')
    args = parser.parse_args()
    padre_conexion, hijo_conexion = multiprocessing.Pipe()
    proceso_hijo = multiprocessing.Process(target=recibir_informacion, args=(hijo_conexion,))
    proceso_hijo.start()
    with open(args.archivo + '.txt', 'r') as archivo:
        for linea in archivo:
            padre_conexion.send(linea)
    padre_conexion.send('fin')
    proceso_hijo.join()
