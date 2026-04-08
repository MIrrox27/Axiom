# author https://github.com/MIrrox27/Axiom
# AxiomWebRequest.py

from axiom.modules.web.AxiomWebModule import *
import json

class Request:
    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body # тело запроса

        self.qwery = {}
        params = []




    def json(self):
        output = {}
        if not self.body:
            return output

        try:
            data = self.body.decode('utf-8')
            output = json.load(data)

        except ValueError:
            return "I dont understand this data-type"

        return output



