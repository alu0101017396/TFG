import math 
import binascii
from urllib.parse import urlparse
from tkinter import *   
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import multiprocessing
import cgi
import binascii
from Robot import *  


class Servidor:
    def __init__(self):
        
        self.Robots = []
        self.Ips = []
        self.depuracion = False

        return
    # Convierte el texto Ascii a binario en forma de byte
    def ascii_binario(self, mensaje):

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

    # Convierte el texto  binario en forma de byte a Asci
    def binario_ascii(self, mensaje):
       # print("mensaje")
       # print(mensaje)
        binary_int = int(mensaje, 2)
        byte_number = binary_int.bit_length() + 7 // 8
        binary_array = binary_int.to_bytes(byte_number, "big")
        ascii_text = binary_array.decode()
        return ascii_text
    
    # Suma los bytes y los devuelve
    def sumarBinario(self, primerNumero, segundoNumero):
        integer_sum = int(primerNumero, 2) + int(segundoNumero, 2)
        binary_sum = bin(integer_sum)    
        return binary_sum   

    # Añade una nueva IP y un nuevo robot a las listas
    def add_ip(self, ip):
      #  print(self.Ips)
        if ip not in self.Ips:
            self.Ips.append(ip)
            self.Robots.append(Robot())
        return

    #Realiza complemento a1 de string
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

    # Calcula el checksum correspondiente al mensaje que se va a enviar
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

    # Comprueba el checksum recibido
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

    def getRespuesta(self, numRobot):
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robots[numRobot].sigOrden = ultimaOrden

        else:
            self.Robots[numRobot].sigOrden = "00110001"

    # Calcula el desplazamiento de las ruedas sobre la superficie
    def calcularDesplazamiento(self, numRobot):  
        self.Robots[numRobot].accion = 0
        primeraMedida = self.Robots[numRobot].historialOrdenes[-4]
        segundaMedida = self.Robots[numRobot].historialOrdenes[-2]
        primeraMedida = float(primeraMedida[: -2])
        segundaMedida = float(segundaMedida[: -2])
        desplazamiento = segundaMedida - primeraMedida
        print("El deslizamiento aproximado es: ")
        print(desplazamiento)

    # Comprueba el mensaje recibido y decide el mensasje que se va enviar
    def controladorRespuesta(self, ip, msj):
        numRobot = self.Ips.index(ip) 
        mensajeCorrecto = self.comprobar_checksum(msj)
        if (mensajeCorrecto == False):
            self.enviarMensajeError(numRobot)
            return
        szChecksum =  len(msj) % 8
        szChecksum += 8
        mensaje = msj[:-szChecksum]
  
       # print(self.Robots)
     
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
            if len(self.Robots[numRobot].pilaOrdenes) != 0:
                ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
                self.Robots[numRobot].pilaOrdenes.pop()
                self.Robots[numRobot].sigOrden = ultimaOrden

            else:
                self.Robots[numRobot].sigOrden = "00110001" 

    # Envia un mensaje de error
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
 
    # Guarda la bateria recibida
    def guardarBateria(self, numRobot, bateria):
        self.Robots[numRobot].bateria = float(bateria)
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robot[numRobot].sigOrden = ultimaOrden

        else:
            self.Robot[numRobot].sigOrden = "00110001"

    # Guarda la distancia recibida
    def guardarDistancia(self, numRobot, distancia):
        self.Robots[numRobot].cm = float(distancia)
        if len(self.Robots[numRobot].pilaOrdenes) != 0:
            ultimaOrden = self.Robots[numRobot].pilaOrdenes[-1]
            self.Robots[numRobot].pilaOrdenes.pop()
            self.Robot[numRobot].sigOrden = ultimaOrden
        else:
            self.Robot[numRobot].sigOrden = "00110001"

    # Posiciona el robot segun los pasos movidos
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
      
      #  print ("1. Listado Ordenes")
      #  print ("2. Calcular deslizamiento")
      #  print ("3. Robots activos")
      #  print ("4. Salir")
        salir = False
        
        #orden = input("Introduce una orden nueva: ")
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
      
        #print ("1. Modo depuracion")
     #   print ("2. Modo normal")
      #  print ("3. Robots activos")
       # print ("4. Salir")
        
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

    # Tarea de calcular el deslizamiento
    def calcular_deslizamiento(self):
        for robot in self.Robots:
            distancia = robot.getMicropasos(10)
            distanciaTraducida = self.ascii_binario(str(distancia))
            robot.accion = 1
            robot.pilaOrdenes.append('01000010' + "0011100100110000" + '00110101')
            robot.pilaOrdenes.append('0011000000110100')

            robot.pilaOrdenes.append('01000110' + "0011100100110000" + '00110101')
            robot.pilaOrdenes.append('0011000000110100')
