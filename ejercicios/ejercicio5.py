#Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.
import argparse
import os
import math
import cmath

def main():

    parser = argparse.ArgumentParser(description='Proceso padre calcula la raíz positiva y proceso hijo calcula la raíz negativa')

    parser.add_argument('-f','--fork',action="store_true", help='Aca se va a pasar el proceso')
    parser.add_argument('-n','--numero',type=int, help='Aca se va a pasar el numero que le vamos a sacar la raiz cuadrada')

    args = parser.parse_args()

    if args.numero:
        if args.fork:
            pid = os.fork()
            if pid > 0:
                print(f"Soy el proceso padre. PID: {os.getpid()}")
                print(f"La raíz cuadrada del número {args.numero} es {math.sqrt(args.numero)}")
            elif pid == 0:
                print(f"Soy el proceso hijo. PID: {os.getpid()}")
                print(f"La raíz cuadrada del número {-args.numero} es {cmath.sqrt(-args.numero)}")
            else:
                print("Se produjo un error al crear el proceso hijo y no se pudo crear un nuevo proceso")
        else:
            print("Falta el argumento '-f'")
    else:
        print("Falta el argumento '-n'")
        exit()

if __name__ == '__main__':
    main()
