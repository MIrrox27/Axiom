# author https://github.com/MIrrox27/Axiom-Language
# AxiomMessengerHandler.py

from http.server import HTTPServer, BaseHTTPRequestHandler
from axiom.modules.LORMS.Messenger.AxiomMessenger import MessengerHTTP




class MessengerHandlerHTTPChat(BaseHTTPRequestHandler):
    default_temp = MessengerHTTP.templates.get('chat')

    def do_GET(self):
        if self.path == '/stream':
            print("/stream")



        try:
            with open(self.default_temp, 'rb') as t:
                content = t.read()

                self.send_response(200)

                self.send_header("Content-type", "text/html")
                #self.send_header("Cache-Control", "no-cache")
                self.end_headers()

                self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File Not Found")


    def _send_headers(self):
        self.send_response()





    def do_POST(self): pass




if __name__ == "__main__":
    server = HTTPServer(('localhost', 1234), MessengerHandlerHTTPChat)
    print("Server started...")
    server.serve_forever()








