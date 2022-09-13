import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii

class Posicion:
    def __init__(self, x = 0, y = 0, orientacion = 0):
        self.x = x
        self.y = y
        self.orientacion = orientacion
        return
    
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_orientacion(self):
        return self.orientacion

