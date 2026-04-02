import http, requests, urllib, webbrowser, socket, ssl
import json, socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler


class WebModule(BaseHTTPRequestHandler):

    def do_GET(self, headers=("Content-type", "text/html; charset=utf-8"), response_body=None):
        self.send_response(200)
        self.send_header(headers[0], headers[1])
        self.end_headers()
        self.wfile.write(response_body.encode("utf-8"))




    def do_POST(self):
        pass




