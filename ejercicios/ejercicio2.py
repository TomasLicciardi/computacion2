import argparse
import sys

parser = argparse.ArgumentParser(description='Repetir tantas veces el texto ingresado como indica el numero ingresado')



parser.add_argument('--cadena', type=str, help='Ingresar texto para repetir')
parser.add_argument('--numero', type=int, help='Ingresar numero para repetir el texto')

args = parser.parse_args()

texto = args.cadena
numero = args.numero

if numero <= 0:
    print("Se ha introducido un numero incorrecto")
    exit()

cadena = []

for i in range(numero):
    cadena.append(texto)

cadena = " ".join(cadena)

print(cadena)