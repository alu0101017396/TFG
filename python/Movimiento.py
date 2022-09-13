import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii

class Movimiento:
    def __init__(self):
        return

    #  Convierte los centimetros en micropasos
    def getMicropasos(self, centimetros):
        stepperResolution = 256
        pasosAMicro = 8
        dosPi = 2 * 3.1416
        radioRueda = 3.2    
        steps = centimetros * stepperResolution * pasosAMicro / (dosPi * radioRueda)
        return steps

    #  Convierte los micropasos en centimetros
    def getCm(self, micropasos):
        stepperResolution = 256
        pasosAMicro = 8
        dosPi = 2 * 3.1416
        radioRueda = 3.2    
        centimetros = micropasos * (dosPi * radioRueda) / pasosAMicro / stepperResolution
        return centimetros
    
    def moverRobot(self, cm, direccion):
        micropasos = self.getMicropasos(cm)
     

        return
        