#!/usr/bin/python

from Tkinter import *
import numpy
import math
from PIL import Image, ImageTk
import operator

# Transmisor de una senal
class Transmitter:
    def __init__(self, ID, canvas, coordinates, strength, color):
        self.id = ID                    # ID del transmisor              
        self.canvas = canvas            # Donde dibujara el canvas
        self.coordinates = coordinates  # Coordenadas del transmisor
        self.strength = strength        # Fuerza de la senal
        self.color = color              # Color de la transmision
        self.i, self.l = self.draw()    # Instancias de los dibujos

    def draw(self):
        x, y = self.coordinates         # Donde se dibujara el transmisor
        t = self.canvas.create_oval((x+5,y+5,x-5,y-5), fill=self.color, outline="black") # Dibujo del transmisor
        l = self.canvas.create_text(x+5, y+5, text="%s: (%d,%d)"%(self.id, x,y))       # Label
        print ("Transmitter: (%d, %d)"%(x, y)) # Mensaje en la terminal
        return t, l                     # Regresamos las instancias de los dibujos en el canvas

# Receptor
class Receiver:
    def __init__(self, canvas, coordinates): 
        self.canvas = canvas            # Donde dibujara el receptor
        self.coordinates = coordinates  # Donde se ubicara el receptor
        self.color = "gray"             # Color de receptor
        self.i = self.draw()            # Dibujo y las instancias del canvas

    def draw(self):
        x, y = self.coordinates         # Donde se dibujara el receptor
        r = self.canvas.create_rectangle((x+5,y+5,x-5,y-5), fill=self.color, outline="black") # Dibujo del receptor
        print ("Receiver: (%d, %d)"%(x, y))   # Mensaje en la terminal
        return r                        # Regresar la instancia del receptor

    def calcDistances(self, transmitters): # Calcular las distancias desde los transmisores al receptor
        x1,y1 = self.coordinates     # Donde esta el receptor
        self.distances = dict()      # Para almacenar las distancias calculadas
        self.di = list()             # Instancias de los dibujos
        self.dl = list()
        self.l = None 
        cont=0     
        for t in transmitters:       # Por cada transmisor detectado
            x2,y2 = t.coordinates    # Tomamos su ubicacion
            distance = round(math.sqrt((x2-x1)**2 + (y2-y1)**2),2) # Calculamos las distancias
            if(distance < t.strength): # Si la distancia es mayor a la fuerza del transmisor
                i = self.canvas.create_oval((x2+distance,y2+distance,x2-distance,y2-distance), outline=t.color, dash=10) # Dibujamos el radio                  # Si no
                self.distances[t.id] = distance # Almacenamos la distancia valida

                l = self.canvas.create_line(x1,y1,x2,y2, fill="black", dash=10) # Creamos una linea desde el transmisor al receptor
                self.di.append(i)   # Guardamos las instancias
                self.dl.append(l)
        

        return

    def setTriCoordinates(self,c): # Para poner las coordenadas detectados por la trilateracion
        print ("coordenada correcta:",c)
        #self.triCoordinates = c    # Coordenadas
        x,y = c     
        self.l = self.canvas.create_text(x+10, y+10, text="Re: (%d,%d)"%(x,y)) # Etiquetamos el receptor
        return

# Para crear la interfaz grafica
# colocar el canvas y demas
class App(Frame):                    
    def __init__(self, parent):      
        Frame.__init__(self, parent)
        self.parent = parent
        self.size = (640,480)
        self.buildGUI() 
        self.parent.config(menu=self.menubar)
        return
        
    def buildGUI(self):
        self.parent.title("Simulacion trilateracion")
        self.pack()

        self.menubar = Menu(self.parent)
        self.menubar.add_command(label="Start", command="start")

        self.canvas = Canvas(self, width=640, height=680)
        image1 = ImageTk.PhotoImage(Image.open('sonivision.png'))
        self.canvas.bind('<Button-1>', callback)
        self.canvas.pack()
        self.canvas.create_image(0,0, image=image1, anchor="nw")
        self.canvas.image = image1


        return
''
# Algoritmo de trilateracion
class Trilateration:            
    def __init__(self, canvas):
        c1, c2, c3, c4, c5, c6, c7, c8, c9, c10= (90,130), (240,110), (340,110), (310,275), (220,340), (150,600), (400,600), (400,435) , (95,270), (100,20) # Coordenadas de los transmisores  /////// EDITAR BEACON ////////////
        global C
        C={'T1':c1,'T2':c2,'T3':c3,'T4':c4,'T5':c5,'T6':c6,'T7':c7 ,'T8':c8,'T9':c9,'T10':c10 }
        self.t1 = Transmitter("T1", canvas, c1, strength=190, color="blue")  # Transmisor 1
        self.t2 = Transmitter("T2", canvas, c2, strength=190, color="blue")  # Transmisor 2
        self.t3 = Transmitter("T3", canvas, c3, strength=190, color="blue")  # Transmisor 3
        self.t4 = Transmitter("T4", canvas, c4, strength=190, color="blue")  # Transmisor 4
        self.t5 = Transmitter("T5", canvas, c5, strength=190, color="blue")  # Transmisor 5
        self.t6 = Transmitter("T6", canvas, c6, strength=190, color="blue")  # Transmisor 6
        self.t7 = Transmitter("T7", canvas, c7, strength=190, color="blue")  # Transmisor 7
        self.t8 = Transmitter("T8", canvas, c8, strength=190, color="blue")  # Transmisor 8
        self.t9 = Transmitter("T9", canvas, c9, strength=190, color="blue")  # Transmisor 9
        self.t10 = Transmitter("T10", canvas, c10, strength=190, color="blue")  # Transmisor 10
        self.receiver = None   # Receptor
        self.canvas = canvas   # Canvas del dibujo

    def setReceiver(self, coordinates): # Colocar el receptor
        x,y = coordinates 
        if(self.receiver is not None):  # Eliminamos todos los dibujos si ya existe un receptor
            self.canvas.delete(self.receiver.i)
            self.canvas.delete(self.receiver.l)
            for i in self.receiver.di:
                self.canvas.delete(i)
            for l in self.receiver.dl:
                self.canvas.delete(l)
        self.receiver = Receiver(self.canvas, coordinates) # Creamos el receptor
        return

    def start(self): # Iniciar la simulacion
        transmitters = [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7 , self.t8 , self.t9, self.t10 ] # Tomamos los transmisores      ///////////// EDITAR BEACON //////////////
        self.receiver.calcDistances(transmitters)  # Calculamos las distancias a los transmisores
        print("Distancias",self.receiver.distances)

        if( 3 <= len(self.receiver.distances)): # Si todos los transmisores estan en el rango

        #//////////////ALGORITMO TRILATERACION ////////////
           # R1,R2,R3=self.receiver.distances

            self.receiver.distances = sorted(self.receiver.distances.items(), key=operator.itemgetter(1)) #Ordena diiccionario por distancia y lo convierte en lista
            self.receiver.distances = self.receiver.distances [0:3] # se sellecionan los tres nodos con distancias menores

            Cor1,R1=self.receiver.distances[0]
            Cor2,R2=self.receiver.distances[1]   # Tomamos nombre de nodo y distancia al receptor
            Cor3,R3=self.receiver.distances[2]
            
            P1 = numpy.array(C[Cor1])        # Almacenamos las coordenadas de cada transmidor
            P2 = numpy.array(C[Cor2])
            P3 = numpy.array(C[Cor3])
            ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))  # Formulas para resolver las ecuaciones de los circulos
            i = numpy.dot(ex, P3 - P1)                   # utilizando algebra lineal
            ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
            ez = numpy.cross(ex,ey)
            d = numpy.linalg.norm(P2 - P1)
            j = numpy.dot(ey, P3 - P1)
            x = (pow(R1,2) - pow(R2,2) + pow(d,2))/(2*d) # Calculamos las coordenadas
            y = ((pow(R1,2) - pow(R3,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x) # usando trilateracion 2D
            tri = P1 + x*ex + y*ey                        # Obtenemos las coordenadas del punto
            self.receiver.setTriCoordinates(tuple(tri))   # asignamos las coordenadas y etiquetamos
            print ("Coordenada recibida:", tri)             # Imprimimos mensajes de aviso al usuario.
            print ("\n")
            self.locationTri(tri)

        elif( 2 == len(self.receiver.distances)):
            R1,R2=self.receiver.distances
            if(self.receiver.distances[R1]<self.receiver.distances[R2]):
                self.Proximidad(R1)
            else:
                self.Proximidad(R2)
        else:
            R1=self.receiver.distances.keys()[0]
            self.Proximidad(R1)


    def Proximidad(self,R):
        nodo=R;
        print("nodo",nodo)
        if(nodo=="T6"):
            print("Usted se encuentra en Contabilidad")
        elif(nodo=="T3"):
            print("Usted se encuentra en Principal")
        elif(nodo=="T7"):
            print("Usted se encuentra en C Principal")
        elif(nodo=="T8"):
            print("Usted se encuentra en Sala2")
        elif(nodo=="T9"):
            print("Usted se encuentra en Recepcion")




    def locationTri(self,tri):
        A,B = tri
        print("location",A,B)
        if(300<A<350 and 160<B<205):
            print("Usted se encuentra en C1")
        elif(350<A<400 and 160<B<205):
            print("Usted se encuentra en C2")
        elif(300<A<350 and 245<B<280):
            print("Usted se encuentra en C3")
        elif(350<A<400 and 245<B<280):
            print("Usted se encuentra en C4")
        elif(300<A<350 and 315<B<355):
            print("Usted se encuentra en C5")
        elif(350<A<400 and 315<B<355):
            print("Usted se encuentra en C6")
        elif(300<A<350 and 355<B<400):
            print("Usted se encuentra en C7")
        elif(350<A<400 and 355<B<400):
            print("Usted se encuentra en C8")
        elif(300<A<350 and 415<B<455):
            print("Usted se encuentra en C9")
        elif(350<A<400 and 415<B<455):
            print("Usted se encuentra en C10")
        elif(220<A<265 and 270<B<315):
            print("Usted se encuentra en C13")
        elif(220<A<265 and 315<B<365):
            print("Usted se encuentra en C12")
        elif(220<A<265 and 365<B<400):
            print("Usted se encuentra en C11")
        elif(300<A<400 and 110<B<160):
            print("Usted se encuentra en R1")
        elif(200<A<250 and 145<B<225):
            print("Usted se encuentra en R2")
        elif(95<A<200 and 180<B<225):
            print("Usted se encuentra en R3")
        elif(95<A<200 and 145<B<180):
            print("Usted se encuentra en R4")
        elif(150<A<270 and 10<B<110):
            print("Usted se encuentra en Sala1")
        elif(300<A<400 and 455<B<495):
            print("Usted se encuentra en Sala2")
        elif(90<A<250 and 110<B<145):
            print("Usted se encuentra en P1")
        elif(250<A<300 and 110<B<270):
            print("Usted se encuentra en P2")
        elif(265<A<300 and 270<B<455):
            print("Usted se encuentra en P2")
        elif(300<A<400 and 200<B<245):
            print("Usted se encuentra en P3")
        elif(300<A<400 and 495<B<600):
            print("Usted se encuentra en C Principal")
        elif(150<A<300 and 455<B<600):
            print("Usted se encuentra en Contabilidad")
        elif(95<A<220 and 225<B<270):
            print("Usted se encuentra en Recepcion")
        elif(270<A<400 and 10<B<110):
            print("Usted se encuentra en Principal")
        elif(95<A<150 and 45<B<110):
            print("Usted se encuentra en Cocina")
        elif(35<A<70 and 20<B<135):
            print("Usted se encuentra en Banos")




def callback(event):
    global tri        # Referencia a la simulacion
    tri.setReceiver((event.x, event.y)) # Colocamos el receptor donde hagamos clic
    tri.start()       # Lanzamos la simulacion
    return

root = Tk()                      # Tkinter
app = App(root)                  # Creamos la instancia de la aplicacion
tri = Trilateration(app.canvas)  # Creamos la instancia de la trilateracion
root.mainloop()                  # Mainloop