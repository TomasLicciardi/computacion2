import http.server
import socketserver
import threading
import multiprocessing
import os
import argparse
from PIL import Image
from multiprocessing import Event, Pipe

class ManejadorProcesamientoImagenes(http.server.SimpleHTTPRequestHandler):
    factor_escala = 1.0
    evento_procesamiento = Event()

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
            mensaje_error = f"Error en la solicitud GET: {e}"
            print(mensaje_error)
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(mensaje_error.encode('utf-8'))
        finally:
            self.evento_procesamiento.set()

    def conversion_escala_grises(self, ruta_imagen):
        try:
            with Image.open(ruta_imagen) as img:
                img_gris = img.convert("L")
                ruta_procesada = "gris_" + os.path.basename(ruta_imagen)
                img_gris.save(ruta_procesada)
                return ruta_procesada
        except Exception as e:
            mensaje_error = f"Error en la conversión a escala de grises: {e}"
            print(mensaje_error)
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
            mensaje_error = f"Error en el escalado de la imagen: {e}"
            print(mensaje_error)
            return None

def iniciar_servidor_http(ip, puerto, handler):
    with socketserver.ThreadingTCPServer((ip, puerto), handler, bind_and_activate=False) as servidor_http:
        servidor_http.allow_reuse_address = True
        servidor_http.server_bind()
        servidor_http.server_activate()
        print(f"Servidor HTTP en {ip}:{puerto}")
        servidor_http.serve_forever()

def iniciar_servidor_procesamiento_imagenes(tuberia, evento_procesamiento):
    try:
        while True:
            factor_escala = tuberia.recv()
            ManejadorProcesamientoImagenes.factor_escala = factor_escala
            evento_procesamiento.wait() 
            evento_procesamiento.clear() 
    except KeyboardInterrupt:
        print("\nDeteniendo servidor de procesamiento de imágenes...")
    except Exception as e:
        mensaje_error = f"Error en el servidor de procesamiento de imágenes: {e}"
        print(mensaje_error)
    finally:
        print("Servidor de procesamiento de imágenes detenido.")

def main():
    parser = argparse.ArgumentParser(description='Tp2 - procesa imágenes')
    parser.add_argument('-i', '--ip', help='Dirección de escucha', required=True)
    parser.add_argument('-p', '--puerto', help='Puerto de escucha', type=int, required=True)
    parser.add_argument('-e', '--escala', help='Factor de escala para redimensionar la imagen', type=float, default=1.0)
    args = parser.parse_args()

    tuberia_servidor, tuberia_cliente = Pipe()
    evento_procesamiento = Event()

    manejador = ManejadorProcesamientoImagenes
    manejador.factor_escala = args.escala
    manejador.evento_procesamiento = evento_procesamiento

    hilo_servidor_http = threading.Thread(target=iniciar_servidor_http, args=(args.ip, args.puerto, manejador), daemon=True)
    hilo_servidor_http.start()

    proceso_procesamiento_imagenes = multiprocessing.Process(target=iniciar_servidor_procesamiento_imagenes, args=(tuberia_servidor, evento_procesamiento))
    proceso_procesamiento_imagenes.start()

    try:
        hilo_servidor_http.join()
        proceso_procesamiento_imagenes.join()
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")

if __name__ == "__main__":
    main()
