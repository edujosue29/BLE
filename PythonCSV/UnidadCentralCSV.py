

import glob													# Librerias
import pandas as pd
import numpy
import operator

mydict = {}
path ='/home/josue/Desktop/Respaldo/DOW/py/BLE/PythonCSV'   # Direccion de archivos CSV
allFiles = glob.glob(path + "/Nodo*.csv")                   # Carga archivos CSV con nombre Nodo
frame = pd.DataFrame()                                      # Definir Estructura de datos
list_ = []

for file_ in allFiles:                                      # Lee multiples CSV y genera la estructura de datos
    df = pd.read_csv(file_,index_col=None, header=0)        # Panda DataFrame
    list_.append(df)
frame = pd.concat(list_)

for x in range(len(frame)):  								# Convierte Estructura dataframe en Diccionario
	currentAxesX = frame.iloc[x,0]							
	currentAxesY = frame.iloc[x,1]
	currentid = frame.iloc[x,2]
	currentDistance = frame.iloc[x,3]
	currentData = [currentAxesX, currentAxesY, currentDistance]
	mydict.setdefault(currentid,[])
	mydict[currentid].append(currentData)

for key, value in mydict.iteritems():						# Algoritmo de Localizacion
	
	if(len(value) >= 3):									# Selecion de algoritmo trilateracion
		print '----------------'
		print key
		print value
		value=sorted(value, key = operator.itemgetter(2)) 	# Ordenar por cercania de nodos
		value = value[0:3]									# Se toman los tres nodos mas cercanos
		A,B,C = value										# Informacion por nodos: Coordenadas, distancia.
		X1,Y1,R1= A 										
		X2,Y2,R2= B
		X3,Y3,R3= C
		C1 = (X1,Y1)
		C2 = (X2,Y2)
		C3 = (X3,Y3)
		P1 = numpy.array(C1)       							
		P2 = numpy.array(C2)
		P3 = numpy.array(C3)
		ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))  		# Formulas para resolver las ecuaciones de los circulos
		i = numpy.dot(ex, P3 - P1)                   		# Algebra lineal
		ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
		ez = numpy.cross(ex,ey)
		d = numpy.linalg.norm(P2 - P1)
		j = numpy.dot(ey, P3 - P1)
		x = (pow(R1,2) - pow(R2,2) + pow(d,2))/(2*d) 		# Calculamos las coordenadas
		y = ((pow(R1,2) - pow(R3,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x) 
		tri = P1 + x*ex + y*ey                        		# Obtenemos las coordenadas del punto
		order=tri[0]										#Ordenar coordenadas
		tri[0]=tri[1]
		tri[1]=order
		print tri

	if(len(value) < 3):										# Seleccion de algoritmo proximidad
		print '********'
		print value
		value=sorted(value, key = operator.itemgetter(2)) 	# Ordenar por cercania de nodos
		X1,Y1,R1 = value[0]									# Se toman el nodo mas cercano
		print key
		print 'Usted Esta Cerca de' , X1 , Y1 , R1





