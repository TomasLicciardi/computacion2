import os
import sys
import argparse

def invertir_linea(linea):
    return ''.join(reversed(linea))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="nombre del archivo")
    args = parser.parse_args()

    try:
        with open(args.file + '.txt', 'r') as archivo:
            lineas = archivo.readlines()
    except Exception:
        print('No se ha encontrado el archivo')
        sys.exit(1)
    

    try:
        for linea in lineas:
            linea = linea.strip()
            conn_pa, conn_hi = os.pipe()
            pid = os.fork()
            if pid == 0:# Proceso hijo
                os.close(conn_hi)
                linea_leida = os.read(conn_pa, 1024).decode().strip()
                os.close(conn_pa)
                linea_invertida = invertir_linea(linea_leida)
                os.write(1, (linea_invertida + '\n').encode())
                sys.exit(0)
            else: # Proceso padre
                os.close(conn_pa)
                os.write(conn_hi, linea.encode())
                os.close(conn_hi)
                os.waitpid(pid, 0)
    except Exception:
        print('Ha ocurrido un error!')