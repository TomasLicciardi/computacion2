import socketserver

# Definir una clase para el manejador del servidor
class UpperCaseHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Recibe los datos del cliente
        data = self.request.recv(1024).strip()
        print(f"Recibido: {data}")

        # Convierte los datos en mayúsculas
        response = data.upper()

        # Envia la respuesta de vuelta al cliente
        self.request.sendall(response + b'\n')

if __name__ == "__main__":
    HOST, PORT = "localhost", 12345

    # Crea un servidor TCP que utiliza hilos para manejar las solicitudes
    server = socketserver.ThreadingTCPServer((HOST, PORT), UpperCaseHandler)

    # Inicia el servidor
    print(f"Servidor escuchando en {HOST}:{PORT}")
    server.serve_forever()
