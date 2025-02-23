import os
import requests
import pandas as pd
from dateutil import parser
from datetime import timedelta

#Funciones
def modificarFechas(fecha):
    #Validamos que la fecha sea un string
    if isinstance(fecha, str):
        #Convertimos la fecha a un objeto datetime
        fecha = parser.isoparse(fecha)

        #Le sumamos 5 horas a la fecha
        fecha += timedelta(hours = 5)

        return fecha
    
    return fecha

if __name__ == '__main__':
    #Definimos flag para volver a traer los datos
    flag = False

    #Definimos la URL para consumir los datos del experimento
    url = 'https://prevebsabackend.azurewebsites.net/api/HealthReports'

    #Consumimos los datos del experimento
    try:
        if flag:
            #Hacemos el request a la URL
            respuesta = requests.get(url)

            #Los leemos como JSON
            data_json = respuesta.json()

            #Convertimos los datos a un DataFrame
            data = pd.DataFrame(data_json)

            #Exportamos los datos
            data.to_excel('datos_experimento.xlsx', index = False)

    except requests.exceptions.RequestException as e:
        print(f'Error al obtener los datos: {e}')

    #Importamos datos del experimento como DataFrame para modificar fechas
    data = pd.read_excel('datos_experimento.xlsx')

    #Sumamos 5 horas a las fechas para ajustar a la hora de Colombia
    data['requestTime'] = list(map(modificarFechas, data['requestTime']))
    data['slackSendTime'] = list(map(modificarFechas, data['slackSendTime']))
    data['errorDetectionTime'] = list(map(modificarFechas, data['errorDetectionTime']))

    print(data)