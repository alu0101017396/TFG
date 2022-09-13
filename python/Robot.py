import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii
from Movimiento import *  
from Posicion import * 
from Sensor import * 

class Robot(Movimiento, Sensor, Posicion):
    def __init__(self, x = 0, y = 0, orientacion = 0):
        Movimiento.__init__(self)
        Sensor.__init__(self)
        Posicion.__init__(self, x, y, orientacion)
        self.pilaOrdenes = []
        self.sigOrden = "00110001"
        self.bateria = 100
        self.historialOrdenes = []
        self.accion = 0
        return
