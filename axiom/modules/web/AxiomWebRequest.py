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



    def json(self):
        output = {}
        if not self.body:
            return output

        try:
           output = json.load(self.body)

        except ValueError:
            return "I dont understand this data-type"

        return output



