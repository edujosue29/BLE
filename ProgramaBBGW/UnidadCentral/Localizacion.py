import glob
import pandas as pd
import numpy

mydict = {}
path = '/home/josue/Desktop/Respaldo/DOW/py/BLE/PythonCSV'  # CSV files path
allFiles = glob.glob(path + "/Nodo*.csv")
frame = pd.DataFrame()
list_ = []

for file_ in allFiles:                                      # Read multiple CSV and make a structure
    df = pd.read_csv(file_,index_col=None, header=0)        # Panda DataFrame
    list_.append(df)
frame = pd.concat(list_)

for x in range(len(frame)):                                 #Dataframe to Dictionary
	currentAxesX = frame.iloc[x,0]							#Order for Asset information
	currentAxesY = frame.iloc[x,1]
	currentid = frame.iloc[x,2]
	currentDistance = frame.iloc[x,3]
	currentData = [currentAxesX, currentAxesY, currentDistance]
	mydict.setdefault(currentid,[])
	mydict[currentid].append(currentData)

for key, value in mydict.iteritems():
	print '----------------'
	print key
	A,B,C = value
	X1,Y1,R1= A
	X2,Y2,R2= B
	X3,Y3,R3= C
	C1 = (X1,Y1)
	C2 = (X2,Y2)
	C3 = (X3,Y3)
	P1 = numpy.array(C1)       # Almacenamos las coordenadas de cada transmidor [x y]
	P2 = numpy.array(C2)
	P3 = numpy.array(C3)
	ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))  # Formulas para resolver las ecuaciones de los circulos
	i = numpy.dot(ex, P3 - P1)                   # utilizando algebra lineal
	ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
	ez = numpy.cross(ex,ey)
	d = numpy.linalg.norm(P2 - P1)
	j = numpy.dot(ey, P3 - P1)
	x = (pow(R1,2) - pow(R2,2) + pow(d,2))/(2*d) # Calculamos las coordenadas
	y = ((pow(R1,2) - pow(R3,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x) # usando trilateracion 2D
	tri = P1 + x*ex + y*ey                        # Obtenemos las coordenadas del punto
	order=tri[0]
	tri[0]=tri[1]
	tri[1]=order
	print tri
