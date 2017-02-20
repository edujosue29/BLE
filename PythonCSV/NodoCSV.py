import csv

with open('Nodo1.csv', 'w') as csvfile:
    fieldnames = ['X', 'Y','Activo', 'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'X': '1', 'Y' :'1' ,'Activo': 'B1', 'Distancia': '10.5'})
    writer.writerow({'X': '1', 'Y' :'1' , 'Activo': 'B2', 'Distancia': '5'})

with open('Nodo2.csv', 'w') as csvfile:
    fieldnames = ['X', 'Y','Activo', 'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'X': '1', 'Y' :'15' , 'Activo': 'B1', 'Distancia': '7.2'})
    writer.writerow({'X': '1', 'Y' :'15' , 'Activo': 'B2', 'Distancia': '9'})

with open('Nodo3.csv', 'w') as csvfile:
    fieldnames = ['X', 'Y','Activo', 'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'X': '15', 'Y' :'15' , 'Activo': 'B1', 'Distancia': '10.5'})
    writer.writerow({'X': '15', 'Y' :'15' , 'Activo': 'B2', 'Distancia': '16'})
    writer.writerow({'X': '15', 'Y' :'15' , 'Activo': 'B3', 'Distancia': '12.6'})


with open('Nodo4.csv', 'w') as csvfile:
    fieldnames = ['X', 'Y','Activo', 'Distancia']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'X': '30', 'Y' :'15' , 'Activo': 'B3', 'Distancia': '1.5'})
    writer.writerow({'X': '30', 'Y' :'15' , 'Activo': 'B2', 'Distancia': '25'})
