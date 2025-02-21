import time
import random
import requests
import threading

#Definimos la URL del microservicio
url = 'http://localhost:5000/ventas'

def envioPeticion(peticion):
    #Validamos si la peticion es GET
    if peticion == 'GET':
        #Hacemos petición GET
        respuesta = requests.get(url, timeout = 5)
    
    #Validamos si la peticion es POST
    elif peticion == 'POST':
        #Creamos un nuevo JSON
        data_json = {"fecha_pedido": "10/10/2021", 
                     "fecha_limite": "10/10/2021", 
                     "estado": 1}
        
        #Hacemos la peticion POST
        respuesta = requests.post(url, json = data_json, timeout = 5)
    
    #De lo contrario es PUT
    else:
        #Editamos siempre la primera venta
        id = 1

        #Creamos JSON para editar
        data_json = {"fecha_pedido": "10/10/2022", 
                     "fecha_limite": "10/10/2022", 
                     "estado": 2}
        
        #URL con la venta a editar
        url_venta = url + '/' + str(id)

        #Hacemos peticion PUT
        respuesta = requests.put(url_venta, json = data_json, timeout = 5)

    return respuesta

def simulacionPeticiones(num_peticiones, intervalo):
    #Definimos arreglo de trheads para hacer cargas simultaneas al microservicio
    threads = []

    #Arreglo de posibles peticiones
    peticiones = ['GET', 'POST', 'PUT']

    #Iteramos para la cantidad de peticiones
    for num in range(num_peticiones):
        #Hacemos que la primera sea POST para que en caso de no haber ventas, se creen
        if not num:
            #Peticion de tipo POST
            peticion = 'POST'
        
        else:
            peticion = random.choice(peticiones)

        #Se realiza la peticion
        t = threading.Thread(target=envioPeticion, args=(peticion,))
        t.start()
        threads.append(t)
        time.sleep(intervalo)
    
    #Espera que los hilos se unan
    for t in threads:
        t.join()

if __name__ == '__main__':
    #Cantidad de petiones a realizar
    num_peticiones = 30

    #Intervalo de tiempo para entre peticiones
    intervalo = 0.5

    #Iniciamos la simulacion
    simulacionPeticiones(num_peticiones, intervalo)


