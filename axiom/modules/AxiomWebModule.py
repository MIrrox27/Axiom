import http, requests, urllib, webbrowser, socket, ssl
import json, socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler

class Output:
    def __init__(self, module):
        self.module = module

    def debug(self, msg, out=False):
        if out: print(f"[DEBUG]: {msg}")

    def error(self, msg, func=None):
        raise Exception(f"[{self.module}]-[{func}]: {msg}")

    def log(self, msg, out=False):
        if out: print(f"[LOG]: {msg}")



class WebHandler(BaseHTTPRequestHandler):

    def do_GET(self, headers=("Content-type", "text/html; charset=utf-8"), response_body=None):
        self.send_response(200)
        self.send_header(headers[0], headers[1])
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))


    def do_POST(self):
        pass




