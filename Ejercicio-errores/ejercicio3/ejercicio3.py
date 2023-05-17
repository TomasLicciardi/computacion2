import argparse

def main():
    try:
        #Creamos el objeto
        parser = argparse.ArgumentParser(description='Contar las lineas, cantidad de palabras, sacar un promedio de la longitud de las palabras del archivo')

        #Le paso los argumentos
        parser.add_argument('--archivo',type=str, help='Poner el archivo')
        args = parser.parse_args()
        
        with open(args.archivo + '.txt', 'r') as archivo:
            lineas = archivo.readlines()
            contador = 0
            while contador < len(lineas):
                if lineas[contador] == '\n':
                    del lineas[contador]
                else:
                    contador += 1
            linea = []
            for i in lineas:
                linea.append(i.strip())
                if i == '\n':
                    lineas.remove(i)
            num_lineas = len(lineas)
            contenido = " ".join(linea)
            palabras = contenido.strip().split()  
            longitud = "".join(palabras)
            promedio = len(longitud) / len(palabras)

        print(f"El archivo tiene {len(palabras)} cantidad de palabras")
        print(f"El archivo tiene {num_lineas} cantidad de lineas")
        print(f"El promedio de la longitud de las palabras es {round(promedio)}")
    except Exception as e:
        with open('errors.log', 'a') as arc_error:
            arc_error.write(str(e) + '\n')
        print('Ha ocurrido un error, fijese en el archivo errors.log')
if __name__ == '__main__':
    main()