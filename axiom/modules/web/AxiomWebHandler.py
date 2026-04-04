# author https://github.com/MIrrox27/Axiom
# AxiomWebHandler

from axiom.modules.web.AxiomWebModule import *

class WebHandler(BaseHTTPRequestHandler):
    router = None


    def do_GET(self):
        router = self.__class__.router
        headers, params = self.__class__.router.match("GET", self.path)

        



    def do_POST(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass
