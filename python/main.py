import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii
from Servidor import *  
#from RequestHandler import RequestHandler_httpd  
import os
msg = ""
msgRecibido = ""
ips = []

servidor = Servidor()

servidor.modos()

class RequestHandler_httpd(BaseHTTPRequestHandler):

   
    # En caso de una peticion Get dependendo de la url redirecciona a la página web
    # recibe el mensaje

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        if self.path == '/':
            self.path = 'Index.html'
            file = self.read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        if self.path == '/Ordenes':
            self.path = 'Ordenes.html'
            file = self.read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        parsed_path = urlparse(self.path)
       

        servidor.add_ip(self.client_address[0])
        numRobot = servidor.Ips.index(self.client_address[0])
        servidor.controladorRespuesta(self.client_address[0], parsed_path.path[1:])
        respuesta = servidor.Robots[numRobot].sigOrden +servidor.calcular_checksum(servidor.Robots[numRobot].sigOrden)
        self.enviarMensaje(respuesta)
        return 
    #Envia respuesta peticion Get
    def enviarMensaje(self, mensaje):
        messagetosend = bytes(mensaje, "utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        return
    #Peticion Post recibidas por la página web, en caso de recibir ordenes las guarda en la pilla de llamada de los robots
    def do_POST(self):
        '''Reads post request body'''
        if self.path == '/guardarOrden':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                numeroOrdenes = 1
                listaOrdenes = []
                while (numeroOrdenes <= 5):

                    if "Orden" + str(numeroOrdenes) in fields:
                        orden = fields.get("Orden" + str(numeroOrdenes))[0]
                        if orden != '':
                            listaOrdenes.append(orden)
                    numeroOrdenes += 1
                self.addOrdenesWeb(listaOrdenes)
               
                self.path = 'Ordenes.html'
                file = self.read_html_template(self.path)
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))
                return
        if self.path == '/calculardeslizamiento':
            servidor.calcular_deslizamiento()
            self.path = 'Index.html'
            file = self.read_html_template('Index.html')
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        self._set_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        msj = self.rfile.read(content_len)
        servidor.add_ip(self.client_address[0])

    #  añade una lista de ordenes a la pila de ordenes de los robots
    def addOrdenesWeb(self, listaOrdenes):
        if len(servidor.Robots) > 0 :
            for orden in listaOrdenes:
                if orden[-1] == "5":
                    numPasos = orden[1:-1]
                    numPasos = int(numPasos)
                    numPasos =servidor.Robots[0].getMicropasos(numPasos)
                    orden = orden[0] + str(numPasos) + "5"
                ordenEnBinario = servidor.ascii_binario(orden)
                for robot in servidor.Robots:
                    robot.pilaOrdenes.append(ordenEnBinario)

    
    def read_html_template(self, path):
        """function to read HTML file"""
        try:
            with open(path) as f:
                file = f.read()
        except Exception as e:
            file = e
        return file








server_address_httpd = ('192.168.1.37', 8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Server started!')
httpd.serve_forever()