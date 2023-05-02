import argparse
import multiprocessing

def invertir_linea(linea):
    return ''.join(reversed(linea))

def recibir_datos(conexion):
    informacion = conexion.recv()
    linea_invertida = invertir_linea(informacion)
    conexion.send(linea_invertida)
    conexion.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="nombre del archivo")
    args = parser.parse_args()

    try:
        with open(args.file + '.txt', 'r') as archivo:
            lineas = archivo.readlines()
            num_lineas = len(lineas)
        archivo.close()
    except Exception:
        print('No se ha encontrado el archivo')

    with open('info_invertida.txt', 'w') as arc_inv:
        for i in range(num_lineas):
            conn_pa, conn_hi = multiprocessing.Pipe()
            proceso_hijo = multiprocessing.Process(target=recibir_datos, args=(conn_hi,))
            proceso_hijo.start()
            conn_pa.send(lineas[i].strip())
            proceso_hijo.join()
            linea_invertida = conn_pa.recv()
            arc_inv.write(linea_invertida + '\n')
            print(linea_invertida)
        