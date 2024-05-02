import http.server
import socketserver
import json

PORT = 8000 # Se define el puerto en el que se ejecutará el servidor HTTP.

class MyRequestHandler(http.server.SimpleHTTPRequestHandler): # Se define una clase que hereda de SimpleHTTPRequestHandler.
    def do_POST(self):
        if self.path == '/': # Si la ruta de solicitud es la raíz, procesa la solicitud.
            content_length = int(self.headers['Content-Length']) # Obtiene la longitud del contenido de la solicitud.
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8')) # Decodifica el contenido de la solicitud.
            message = data['data']
            print(f"Received message: {message}") # Imprime el mensaje recibido.
            self.send_response(200)
            self.send_header('Content-type', 'text/html') # Responde con un código de estado 200 y un mensaje de confirmación.
            self.end_headers()
            self.wfile.write(b"Message received")
        else:
            self.send_response(404) # Si la ruta de solicitud no es la raíz, responde con un código de estado 404.
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not Found")

Handler = MyRequestHandler # Se define el manejador de solicitudes.

with socketserver.TCPServer(("", PORT), Handler) as httpd: # Se crea un servidor TCP.
    print(f"Serving at port {PORT}")
    httpd.serve_forever() # Se inicia el servidor.