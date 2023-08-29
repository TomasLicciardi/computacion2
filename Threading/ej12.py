import multiprocessing, os, threading

def receptor():
    x = 0
    with open(fifo_1, "r") as fifo:
        lineas = fifo.readlines()
        lineas = [linea.strip() for linea in lineas]
        for linea in lineas:
            hilo = threading.Thread(target=funcion_del_hilo, args=(linea,))
            hilo.start()
            x += 1
            if x != 1:
                hilo.join()

def funcion_del_hilo(linea):
    numero_de_caracteres = len(linea)
    print(f"La linea {linea} tiene {numero_de_caracteres} caracteres")

if __name__ == '__main__':

    fifo_1 = "mi_fifo"

    if os.path.exists(fifo_1):
        os.remove(fifo_1)

    os.mkfifo(fifo_1)

    proceso_2 = multiprocessing.Process(target=receptor)
    proceso_2.start()
