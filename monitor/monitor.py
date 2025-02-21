import time
import requests
from datetime import datetime
import signal

contador = 0
ejecutando = True


def interrupcion(sig, frame):
    global ejecutando
    ejecutando = False

def Monitor_Init():
    global contador
    respuesta = EstadoConexion()


    if respuesta == 200:
        contador = 0 
        print(datetime.now(), "Conexión normal con el microservicio de ventas")
    else:
        contador += 1

    if contador > 0:
        if contador < 3:
            print(datetime.now(), "No se recibe respuesta del microservicio de ventas, reintento nro: ", contador)
        else:
            print(datetime.now(),"\U000026A0", "ALERTA EL SERVIDOR DE VENTAS ESTÁ CAIDO","\U0001F6A8","\U0001F6A8")


def EstadoConexion():
    URL = 'http://localhost:5000/ventas'
    tiempo = 3
    try:
        respuesta = requests.get(URL, timeout = tiempo).status_code 
    except Exception as e:
        respuesta = 0

    return respuesta

signal.signal(signal.SIGINT, interrupcion)

while ejecutando:
    Monitor_Init()
    time.sleep(3)

print("Se detuvo el monitor")