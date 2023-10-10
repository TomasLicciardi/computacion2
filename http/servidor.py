import http.server
import socketserver

PORT = 1111

# Mapea las rutas a los archivos HTML
rutas = {
    '/': 'index.html',
    '/primera.html': 'primera.html',
    '/segunda.html': 'segunda.html'
}

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in rutas:
            file = rutas[self.path]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open(file, 'rb') as archivo:
                self.wfile.write(archivo.read())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b'<h1>404 - Page Not Found</h1>')

socketserver.TCPServer.allow_reuse_address = True

myhttphandler = MyHandler

httpd = http.server.HTTPServer(("", PORT), myhttphandler)

print(f"Abriendo servidor en el puerto: {PORT}")

httpd.serve_forever()
