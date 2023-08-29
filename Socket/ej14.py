import socket
import threading

def atender_conexion(conexion):
    while True:
        mensaje = conexion.recv(1024)

        if mensaje == b"quit":
            conexion.close()
            break

        print(f"Mensaje del cliente: {mensaje}")

def main():
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(("127.0.0.1", 8080))
    socket_servidor.listen(1)

    while True:
        conexion, _ = socket_servidor.accept()

        hilo = threading.Thread(target=atender_conexion, args=(conexion,))
        hilo.start()

if __name__ == "__main__":
    main()
