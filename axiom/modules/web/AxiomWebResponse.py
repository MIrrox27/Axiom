# author https://github.com/MIrrox27/Axiom
# AxiomWebResponse.py


from axiom.modules.web.AxiomWebModule import *
import json

class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body


    def json(self, data):
        self.body = json.dumps(data)
        self.headers = {"Content-Type": "application/json"}


    def html(self, content):
        self.body = content
        self.headers = {"Content-Type": "text/html"}


    def redirect(self, url):
        self.status = 302
        self.headers = {"Location": url}





