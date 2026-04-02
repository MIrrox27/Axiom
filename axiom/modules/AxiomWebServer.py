from axiom.modules.AxiomWebModule import WebModule
from http.server import HTTPServer, SimpleHTTPRequestHandler

class ServerModule(WebModule):
    def serve(self, host_name='localhost', port=8080, handler=SimpleHTTPRequestHandler):  # функция для развертывания веб-сервера
        server = HTTPServer((host_name, port), handler)
        server.serve_forever()