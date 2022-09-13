import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii





#  More details.
class Mapa:
    def __init__(self, top):
        self.puntos = []      
        self.my_canvas = Canvas(top, bg = "white", width = "800", height = "800")  
        return
    def set_punto(self, x , y, orientacion, distancia):
        self.puntos.append(Punto(x , y, orientacion, distancia))
        return
    def crear_mapa(self):
        for i in range(1, len(self.puntos), 1):    
            self.my_canvas.create_line(self.puntos[i - 1].x, self.puntos[i - 1].y, self.puntos[i].x, self.puntos[i].y, fill ="red")
            print(self.puntos[i - 1].x)
            print(self.puntos[i - 1].y)
            print(self.puntos[i].x)
            print(self.puntos[i].y)
        return

class Punto:
    def __init__(self, xOrigen = 0, yOrigen = 0, orientacion = 0, distancia = 0):
        self.x = distancia * math.cos(orientacion) + xOrigen
        self.y = distancia * math.sin(orientacion) + yOrigen
        return

