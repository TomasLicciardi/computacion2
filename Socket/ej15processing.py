import socket
import multiprocessing

def atender_conexion(conexion):
    while True:
        mensaje = conexion.recv(1024)

        if mensaje == b"exit":
            conexion.close()
            break

        respuesta = mensaje.upper()
        conexion.sendall(respuesta)

def main():
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(("127.0.0.1", 8080))
    socket_servidor.listen(1)

    while True:
        conexion, _ = socket_servidor.accept()

        proceso = multiprocessing.Process(target=atender_conexion, args=(conexion,))
        proceso.start()

if __name__ == "__main__":
    main()
