# author https://github.com/MIrrox27/Axiom

from axiom.modules.web.AxiomWebModule import WebHandler, Output
from http.server import HTTPServer


class ServerModule(WebHandler):
    def __init__(self):
        self.output = Output('ServerModule')

    def serve(self, host_name, port, handler, debug=False):  # функция для развертывания веб-сервера
        server = HTTPServer((host_name, port), handler)
        self.output.debug(f"Server is starting: http://{host_name}:{port}", out=debug)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            self.output.log('Server operation is corrupted', out=True)

        server.server_close()
        self.output.log('The server has stopped', out=True)






if __name__ == "__main__":
    server = ServerModule()
    server.serve(host_name='localhost', port=8080, debug=True)