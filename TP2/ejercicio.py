import http.server
import socketserver
import socket
import threading
import multiprocessing
import os
import argparse
from PIL import Image

class ManejadorProcesamientoImagenes(http.server.SimpleHTTPRequestHandler):
    factor_escala = 1.0

    def do_GET(self):
        try:
            ruta_imagen = self.path[1:]

            if self.factor_escala == 1.0:
                ruta_procesada = self.conversion_escala_grises(ruta_imagen)
            else:
                ruta_procesada = self.escalar_imagen(ruta_imagen, self.factor_escala)

            if ruta_procesada:
                with open(ruta_procesada, 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(f.read())
            else:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"Error en el servidor: no se pudo procesar la imagen")
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
        except Exception as e:
            print(f"Error en la solicitud GET: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error en el servidor: {e}".encode('utf-8'))

    def conversion_escala_grises(self, ruta_imagen):
        try:
            with Image.open(ruta_imagen) as img:
                img_gris = img.convert("L")
                ruta_procesada = "gris_" + os.path.basename(ruta_imagen)
                img_gris.save(ruta_procesada)
                return ruta_procesada
        except Exception as e:
            print(f"Error en la conversión a escala de grises: {e}")
            return None

    def escalar_imagen(self, ruta_imagen, factor_escala):
        try:
            with Image.open(ruta_imagen) as img:
                ancho, alto = img.size
                nuevo_ancho = int(ancho * factor_escala)
                nuevo_alto = int(alto * factor_escala)
                img_escalada = img.resize((nuevo_ancho, nuevo_alto))
                ruta_procesada = "escalada_" + os.path.basename(ruta_imagen)
                img_escalada.save(ruta_procesada)
                return ruta_procesada
        except Exception as e:
            print(f"Error en el escalado de la imagen: {e}")
            return None

def iniciar_servidor_http(ip, puerto, handler):
    with socketserver.ThreadingTCPServer((ip, puerto), handler) as servidor_http:
        print(f"Servidor HTTP en {ip}:{puerto}")
        servidor_http.serve_forever()

def iniciar_servidor_procesamiento_imagenes(servidor_http):
    socket_comunicacion = None
    try:
        socket_comunicacion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_comunicacion.bind(('localhost', 9999))
        socket_comunicacion.listen(1)

        while True:
            conexion, direccion = socket_comunicacion.accept()
            factor_escala = float(conexion.recv(1024).decode('utf-8'))
            conexion.close()
            ManejadorProcesamientoImagenes.factor_escala = factor_escala

    except KeyboardInterrupt:
        print("\nDeteniendo servidor de procesamiento de imágenes...")
    except Exception as e:
        print(f"Error en el servidor de procesamiento de imágenes: {e}")
    finally:
        if socket_comunicacion:
            socket_comunicacion.close()
            print("Servidor de procesamiento de imágenes detenido.")

def main():
    parser = argparse.ArgumentParser(description='Tp2 - procesa imágenes')
    parser.add_argument('-i', '--ip', help='Dirección de escucha', required=True)
    parser.add_argument('-p', '--puerto', help='Puerto de escucha', type=int, required=True)
    parser.add_argument('-e', '--escala', help='Factor de escala para redimensionar la imagen', type=float, default=1.0)
    args = parser.parse_args()

    manejador = ManejadorProcesamientoImagenes
    manejador.factor_escala = args.escala
    hilo_servidor_http = threading.Thread(target=iniciar_servidor_http, args=(args.ip, args.puerto, manejador), daemon=True)
    hilo_servidor_http.start()

    proceso_procesamiento_imagenes = multiprocessing.Process(target=iniciar_servidor_procesamiento_imagenes, args=(manejador,))
    proceso_procesamiento_imagenes.start()

    try:
        hilo_servidor_http.join()
        proceso_procesamiento_imagenes.join()
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")

if __name__ == "__main__":
    main()
