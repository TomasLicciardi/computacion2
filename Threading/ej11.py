import threading
import queue
import codecs

def leer_texto():
    texto = input("Ingrese un texto: ")
    cola.put(texto)

def encriptar_texto():
    texto_encriptado = ""
    for letra in cola.get():
        if letra >= "A" and letra <= "Z":
            letra_encriptada = codecs.encode(letra, "rot13")
        elif letra >= "a" and letra <= "z":
            letra_encriptada = codecs.encode(letra, "rot13")
        else:
            letra_encriptada = letra
            texto_encriptado += letra_encriptada
    cola.put(texto_encriptado)

def mostrar_texto():
    texto_encriptado = cola.get()
    print(f"Texto encriptado: {texto_encriptado}")

cola = queue.Queue()

h1 = threading.Thread(target=leer_texto)
h2 = threading.Thread(target=encriptar_texto)
h3 = threading.Thread(target=mostrar_texto)

if __name__ == '__main__':
    h1.start()
    h2.start()
    h3.start()

    h1.join()
    h2.join()
    h3.join()