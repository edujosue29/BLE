import blescan														# Importar Librerias
import sys
import time
import csv
import math
import bluetooth._bluetooth as bluez

BLE_dict = {}														# Diccionario de Beacons
dev_id = 0
A=55																# RSSI a 1m
n=2.5 																#Condiciones del medio
try:																# coneccion con adaptador bluetooth
	sock = bluez.hci_open_dev(dev_id)						
	print "ble thread started"

except:
	print "error accessing bluetooth device..."

blescan.hci_le_set_scan_parameters(sock)							# Definir bluetooth como BLE
blescan.hci_enable_le_scan(sock)									# Habilita lector BLE
while True:
	BLE_dict = {}
	cont=0;
	while(cont<30):													# Cantidad de muestras
		returnedList = blescan.parse_events(sock, 10)				# Lista de datos lectura BLE
	
		for beacon in returnedList:
            print "----------"
			BLE_ID = beacon[0:17]									#Seleccion de MAC address
            BLE_RSSI = beacon[62:65]								#Seleccion de RSSI
            if(BLE_ID[0:5] == '24:71'):
				BLE_dict.setdefault(BLE_ID,[]).append(BLE_RSSI)         #Diccionario con informacion por activo 
			print BLE_ID
			print BLE_RSSI
			print BLE_dict
		cont=cont+1
		print cont

	with open('/var/www/html/Nodo1.csv', 'w') as csvfile:   		#Genera archivo CSV
		fieldnames = ['X','Y','Activo', 'Distancia']						#Columnas
   		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)		#Se abre archivo en modo escritura
		writer.writeheader()
		for key, value in BLE_dict.iteritems():						# Almacenar Informacion en CSV
			print "RESULTADO"
			print value
			value = map(int,value)
			Name = key
			sortedLst = sorted(value)
            LenValue = len(value)
            index = (LenValue-1)//2
            if(LenValue%2):
            	Media= sortedLst[index]
            else:
                Media= (sortedLst[index] +sortedLst[index+1])/2
            Media = 10**(-((Media+A)/(10*n)))
   			Media = round(Media)
   			writer.writerow({'X': 25,'Y':25,'Activo': Name, 'Distancia': Media}) 					
	time.sleep(5)

