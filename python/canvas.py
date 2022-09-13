import clases
from tkinter import *   
from random import seed
from random import randint
# seed random number generator

top = Tk()  
  
top.geometry("800x800")  

mapa = clases.Mapa(top)   
#seed(1)
# generate some integers
#for _ in range(10):
#	mapa.puntos.append(clases.Punto(randint(200, 400),  randint(200, 400), randint(0, 360), randint(0, 100)))


#mapa.crear_mapa()
#mapa.my_canvas.pack()  
  
top.mainloop()  


    