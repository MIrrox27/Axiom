# author https://github.com/MIrrox27/Axiom
# Общие основные классы

import http, requests, urllib, webbrowser, socket, ssl
import json, socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

from axiom.modules.web import AxiomWebRouter, AxiomWebRequest, AxiomWebResponse

class Output:
    def __init__(self, module):
        self.module = module

    def debug(self, msg, out=False):
        if out: print(f"[DEBUG]: {msg}")

    def error(self, msg, func=None):
        raise Exception(f"[{self.module}]-[{func}]: {msg}")

    def log(self, msg, out=False):
        if out: print(f"[LOG]: {msg}")







