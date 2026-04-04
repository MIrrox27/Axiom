from http.server import HTTPServer, BaseHTTPRequestHandler
from axiom.modules.LORMS.Messenger.AxiomMessenger import MessengerHTTP




class MessengerHandlerHTTPChat(BaseHTTPRequestHandler):
    temp = Messenger.templates.get('chat.html')

    def do_GET(self):
        try:

            with open(self.temp, 'rb') as t:
                content = t.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File Not Found")


