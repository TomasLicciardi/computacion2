#Realizar un programa que implemente fork junto con el parseo de argumentos. Deberá realizar un fork si -f aparece entre las opciones al ejecutar el programa. El proceso padre deberá calcular la raiz cuadrada positiva de un numero y el hijo la raiz negativa.
import argparse
import os
import math

def main():

    parser = argparse.ArgumentParser(description='Proceso padre calcula la raíz positiva y proceso hijo calcula la raíz negativa')

    parser.add_argument('-f','--fork", action="store_true', help='Aca se va a pasar el argumento -f para que se cree un proceso hijo')
    parser.add_argument('-n','--numero',type=int, help='Aca se va a pasar el numero que le vamos a sacar la raiz cuadrada')

    args = parser.parse_args()

    if args.numero > 0:
        if args.fork:
            pid = os.fork()
            if pid > 0:
                print(f"Soy el proceso padre. PID: {os.getpid()}")
                resultado = round(math.sqrt(args.numero),2)
                print(f"La raíz cuadrada del número {args.numero} es {resultado}")
            elif pid == 0:
                print(f"Soy el proceso hijo. PID: {os.getpid()}")
                resultado = str(round(math.sqrt(args.numero),2)) + 'j'
                print(f"La raíz cuadrada del número {-args.numero} es {resultado}")
            else:
                print("Se produjo un error al crear el proceso hijo y no se pudo crear un nuevo proceso")
        else:
            print("Falta el argumento '-f'")
    else:
        print("Ha ingresado mal el argumento")
        exit()

if __name__ == '__main__':
    main()
