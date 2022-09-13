import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii
msg = ""
msgRecibido = ""
ips = []

def getMicropasos( centimetros):
    stepperResolution = 256
    pasosAMicro = 8
    dosPi = 2 * 3.1416
    radioRueda = 3.2    
    steps = centimetros * stepperResolution * pasosAMicro / (dosPi * radioRueda)
    return steps
def getCm( micropasos):
    stepperResolution = 256
    pasosAMicro = 8
    dosPi = 2 * 3.1416
    radioRueda = 3.2    
      #  steps = centimetros * stepperResolution * pasosAMicro / (dosPi * radioRueda)
    centimetros = micropasos * (dosPi * radioRueda) / pasosAMicro / stepperResolution
    return centimetros
class Movimiento:
    def __init__(self):
        return
    def getMicropasos(self, centimetros):
        stepperResolution = 256
        pasosAMicro = 8
        dosPi = 2 * 3.1416
        radioRueda = 3.2    
        steps = centimetros * stepperResolution * pasosAMicro / (dosPi * radioRueda)
        return steps
    def getCm(self, micropasos):
        stepperResolution = 256
        pasosAMicro = 8
        dosPi = 2 * 3.1416
        radioRueda = 3.2    
      #  steps = centimetros * stepperResolution * pasosAMicro / (dosPi * radioRueda)
        centimetros = micropasos * (dosPi * radioRueda) / pasosAMicro / stepperResolution
        return centimetros
    
    def moverRobot(self, cm, direccion):
        micropasos = self.getMicropasos(cm)
     

        return
        
class Sensor:
    def __init__(self):
        self.cm = 0
        return


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

class Punto:
    def __init__(self, xOrigen = 0, yOrigen = 0, orientacion = 0, distancia = 0):
        self.x = distancia * math.cos(orientacion) + xOrigen
        self.y = distancia * math.sin(orientacion) + yOrigen
        return

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



class Servidor:
    def __init__(self):
        
        self.Robots = []
        self.Ips = []
        self.depuracion = False
#        for _ in numeroRobots:
#            self.Robots.append(Robot())
        return

    def ascii_binario(self, mensaje):
        #l,m=[],[]
        #for i in mensaje:
       #     l.append(ord(i))
       # for i in l:
       #     algo = bin(i)[2:].zfill(8)
       #     m.append(int(algo))
        byte_array = mensaje.encode()

        binary_int = int.from_bytes(byte_array, "big")
        binario = bin(binary_int) 
        binary_string =  format(binary_int, '#010b')
        binary_string = binary_string[2:]
        resto =  len(binary_string) % 8
        if (resto != 0):
            while(resto != 0):
                resto -= 1
                binary_string = "0" + binary_string
        return binary_string
       # return bin(int.from_bytes(mensaje.encode(), 'big'))


    def binario_ascii(self, mensaje):
        print("mensaje")
        print(mensaje)
        binary_int = int(mensaje, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode()
        return ascii_text
    
    def sumarBinario(self, primerNumero, segundoNumero):
        integer_sum = int(primerNumero, 2) + int(segundoNumero, 2)
        binary_sum = bin(integer_sum)    
        return binary_sum   

    def add_ip(self, ip):
        print(self.Ips)
        if ip not in self.Ips:
            self.Ips.append(ip)
            self.Robots.append(Robot())
        return
    def ca1(self, binario):
        i = 0
        binariList = list(binario)
        while i < len(binariList):
            if (binariList[i] == "1"):
                binariList[i] = "0"
            else:
                binariList[i] = "1"
            i +=1
        return "".join(binariList)
    def calcular_checksum(self, mensaje):
        numMensajes =  len(mensaje) / 8 
        i = 0
        suma = "00000000"
        #suma = 0
        while (i < numMensajes):
            suma = self.sumarBinario(suma,mensaje[i * 8:i * 8 + 8])
            i += 1
        suma = self.ca1(suma[2:])
        if (len(suma) < 8):
            suma = suma.rjust(8, '1')
        return suma

    def comprobar_checksum(self, mensaje):
        leng = len(mensaje)
        szChecksum = leng % 8 
        szChecksum += 8
        checksum = mensaje[-szChecksum:]
      #  print("checksum", checksum)
        msjSinCheck = mensaje[:-szChecksum]
       # print("msj", msjSinCheck)
        numMensajes = len(msjSinCheck) / 8
        i = 0
        suma = "00000000"
        while (i < numMensajes):
            suma = self.sumarBinario(suma,msjSinCheck[i * 8:i * 8 + 8])
            i += 1
        suma = self.ca1(suma[2:])
      #  print("msj", suma)
        if (len(suma) < szChecksum):
            suma = suma.rjust(szChecksum, '1')
        if (suma == checksum):
            return True
        else:
            return False

#00110100
#00110000
#01100100
    def getRespuesta(self, numRobot):
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robots[numRobot].sigOrden = ultimaOrden

        else:
            self.Robots[numRobot].sigOrden = "00110001"

    def calcularDesplazamiento(self, numRobot):
        #print("Historial")
        #print(self.Robots[numRobot].historialOrdenes)
        self.Robots[numRobot].accion = 0
        primeraMedida = self.Robots[numRobot].historialOrdenes[-4]
        segundaMedida = self.Robots[numRobot].historialOrdenes[-2]
        primeraMedida = float(primeraMedida[: -2])
        segundaMedida = float(segundaMedida[: -2])
        desplazamiento = segundaMedida - primeraMedida
        print("El deslizamiento aproximado es: ")
        print(desplazamiento)

    def controladorRespuesta(self, ip, msj):
        numRobot = self.Ips.index(ip) 
        mensajeCorrecto = self.comprobar_checksum(msj)
        if (mensajeCorrecto == False):
            self.enviarMensajeError(numRobot)
            return
        szChecksum =  len(msj) % 8
        szChecksum += 8
        mensaje = msj[:-szChecksum]
       # comprobacion = self.comprobar_checksum(msj)
     #   print(comprobacion)
     #   if (self.Robots[numRobot].accion != 1):
      #      self.calcular_deslizamiento()
        print(self.Robots)
      #  if len(self.Robots[numRobot].pilaOrdenes) > 0:
      #      ultimaOrden =  self.Robots[numRobot].pilaOrdenes[len(self.Robots[numRobot].pilaOrdenes) - 1]
        mensajeAscii = self.binario_ascii(mensaje)
        msj = mensajeAscii.replace('\x00','')

        funcion = msj[-1]
        self.Robots[numRobot].historialOrdenes.append(msj)
        if (len(self.Robots[numRobot].pilaOrdenes) == 0 and self.Robots[numRobot].accion == 1):
            self.calcularDesplazamiento(numRobot)
        if (funcion == "/"):
            return
        elif (funcion == "0"):
             self.ErrorAccion(numRobot)     
        elif (funcion == "1"):
            self.getRespuesta(numRobot)
        elif (funcion == "2"):
            self.accionCompletada(numRobot)
        elif (funcion == "3"):
            self.guardarBateria(numRobot)
        elif (funcion == "4"):
            self.guardarDistancia(numRobot, msj[0:-2])
        elif (funcion == "5"):
            self.pasosMovidos(numRobot)
        else:
            self.Robot[numRobot].sigOrden = "00110001" 
    def enviarMensajeError(self,numRobot):

            self.Robots[numRobot].sigOrden = "00101111"

   
         
    def accionCompletada(self, numRobot):
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robots[numRobot].sigOrden = ultimaOrden

        else:
            self.Robots[numRobot].sigOrden = "00110001"

    def ErrorAccion(self, numRobot):
        if len(self.Robots[numRobot].pilaOrdenes) != 0 :
            mensaje = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robots[numRobot].sigOrden = mensaje
        else:
            self.Robots[numRobot].sigOrden = "00110001"
 
 #   def esperaOrden(self):
 #       if len(self.Robots[numRobot].pilaOrdenes) != 0:
 #           ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
 #           self.Robots[numRobot].pilaOrdenes.pop()
 #           self.Robot[numRobot].sigOrden = ultimaOrden

#        else:
#            self.Robot[numRobot].sigOrden = "00110001"

    def guardarBateria(self, numRobot, bateria):
        self.Robots[numRobot].bateria = float(bateria)
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robot[numRobot].sigOrden = ultimaOrden

        else:
            self.Robot[numRobot].sigOrden = "00110001"

    def guardarDistancia(self, numRobot, distancia):
        self.Robots[numRobot].cm = float(distancia)
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robot[numRobot].sigOrden = ultimaOrden
        else:
            self.Robot[numRobot].sigOrden = "00110001"

    def pasosMovidos(self, numRobot):
        ultimaOrden = self.Robots[numRobot].historialOrdenes[-1]
        ordenTraducida = self.binario_ascii(ultimaOrden)
        distanciaCm = self.Robots[numRobot].getCm(float(ordenTraducida[1:-1]))
        if (ordenTraducida[0] == 'F'):
            self.Robots[numRobot].y += distanciaCm
        elif (ordenTraducida[0] == 'B'):
            self.Robots[numRobot].y -= distanciaCm
        elif (ordenTraducida[0] == 'R'):
            self.Robots[numRobot].x += distanciaCm
        elif (ordenTraducida[0] == 'L'):
            self.Robots[numRobot].x -= distanciaCm
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robot[numRobot].sigOrden = ultimaOrden

        else:
            self.Robot[numRobot].sigOrden = "00110001"

       # self.Robots.Posicion.x
    def menuOrdenes(self):
        orden = 0
      
        print ("1. Listado Ordenes")
        print ("2. Calcular deslizamiento")
        print ("3. Robots activos")
        print ("4. Salir")
        salir = False
        
        orden = input("Introduce una orden nueva: ")
        while salir == False:
            if orden == 1:
                print ("Opcion 1")
            elif orden == 2:
                self.calcular_deslizamiento()
            elif orden == 3:
                print (self.Robots)
                print (self.Ips)
            elif orden == 4:
                salir = True
            else:
                for robot in self.Robots:
                    robot.mensaje = orden
                salir = True
    def modos(self):
        opcion = 0
      
        print ("1. Modo depuracion")
        print ("2. Modo normal")
        print ("3. Robots activos")
        print ("4. Salir")
        
        self.depuracion = False

        #opcion = input("Introduce una orden nueva: ")
        if opcion == "1":
            print("entro")
            self.depuracion = True
        elif opcion == "2":
            self.depuracion = False
        elif opcion == "3":
            print("Opcion 3")
        elif opcion == "4":
            salir = True
    def calcular_deslizamiento(self):
        for robot in self.Robots:
            distancia = robot.getMicropasos(10)
            distanciaTraducida = self.ascii_binario(str(distancia))
            robot.accion = 1
            robot.pilaOrdenes.append('01000010' + "0011000100110000" + '00110101')
            robot.pilaOrdenes.append('0011000000110100')

            robot.pilaOrdenes.append('01000110' + "0011000100110000" + '00110101')
            robot.pilaOrdenes.append('0011000000110100')


    def addOrdenesWeb(self, listaOrdenes):
        for orden in listaOrdenes:
            if orden[-1] == "5":
                numPasos = orden[1:-1]
                numPasos = int(numPasos)
                numPasos = getMicropasos(numPasos)
                orden = orden[0] + str(numPasos) + "5"
            ordenEnBinario = self.ascii_binario(orden)
            for robot in self.Robots:
                robot.pilaOrdenes.append(ordenEnBinario)




servidor = Servidor()

servidor.modos()
import os

def read_html_template(path):
    """function to read HTML file"""
    try:
        with open(path) as f:
            file = f.read()
    except Exception as e:
        file = e
    return file
class RequestHandler_httpd(BaseHTTPRequestHandler):

   

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        if self.path == '/':
            self.path = 'Index.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        if self.path == '/Ordenes':
            self.path = 'Ordenes.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        parsed_path = urlparse(self.path)
       
      #  if servidor.depuracion == True:
       #     servidor.menuOrdenes()
       
        print("llego: ", parsed_path.path[1:])
        servidor.add_ip(self.client_address[0])
        numRobot = servidor.Ips.index(self.client_address[0])
        servidor.controladorRespuesta(self.client_address[0], parsed_path.path[1:])
        respuesta = servidor.Robots[numRobot].sigOrden + servidor.calcular_checksum(servidor.Robots[numRobot].sigOrden)
       # respuesta = servidor.getRespuesta(self.client_address[0])
        print("respuesta")
        print(respuesta)
        self.enviarMensaje(respuesta)
        return 
    def enviarMensaje(self, mensaje):
        messagetosend = bytes(mensaje, "utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        return
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
                servidor.addOrdenesWeb(listaOrdenes)
                # create table User if it runs first time else not
               
                # insert record into User table
                self.path = 'Ordenes.html'
                file = read_html_template(self.path)
                self.send_response(200, "OK")
                self.end_headers()
                self.wfile.write(bytes(file, "utf-8"))
                return
        if self.path == '/calculardeslizamiento':
            servidor.calcular_deslizamiento()
            self.path = 'Index.html'
            file = read_html_template(self.path)
            self.send_response(200, "OK")
            self.end_headers()
            self.wfile.write(bytes(file, "utf-8"))
            return
        self._set_headers()
        content_len = int(self.headers.getheader('content-length', 0))
        msj = self.rfile.read(content_len)
        servidor.add_ip(self.client_address[0])
        #respuesta = servidor.controladorRespuesta(self.client_address[0], parsed_path.path[1:])
       # client_address[0]
        #calcular_deslizamiento(msgRecibido)
        
        #self.wfile.write("received post request:<br>{}".format(post_body))
        return


server_address_httpd = ('192.168.1.37', 8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Server started!')
httpd.serve_forever()



