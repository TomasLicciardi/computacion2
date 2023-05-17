import multiprocessing
import argparse

def recibir_informacion_hijo(conexion_hijo):
    while True:
        linea = conexion_hijo.recv()
        if linea == 'fin':
            break
        

def recibir_informacion_nieto(conexion_nieto):
    while True:
        informacion = conexion_nieto.recv()
        if informacion == 'fin':
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Proceso padre lee un archivo de texto y envia cada linea al proceso hijo a traves de un pipe. El proceso hijo recibe las lineas y cuenta la cantidad de palabras que contiene')
    parser.add_argument('-a','--archivo',type=str, help='Aca se va a pasar el archivo que vamos a leer')
    args = parser.parse_args()
    conexion_padre,conexion_hijo = multiprocessing.Pipe()
    conexion_hijo, conexion_nieto = multiprocessing.Pipe()
    proceso_hijo = multiprocessing.Process(target=recibir_informacion_hijo,args=(conexion_hijo,))
    proceso_nieto = multiprocessing.Process(target=recibir_informacion_nieto,args=(conexion_nieto,))
    proceso_hijo.start()
    with open(args.archivo + '.txt', 'r') as archivo:
        for linea in archivo:
            conexion_padre.send(linea)
    conexion_padre.send('fin')
    proceso_hijo.join()
