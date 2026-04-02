import http, requests, urllib, webbrowser, socket, ssl
import json, socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler


class WebModule(BaseHTTPRequestHandler):

    def do_GET(self, headers=["Content-type", "text/html; charset=utf-8"]):
        pass

    def do_POST(self):
        pass




