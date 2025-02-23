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
    flag = True

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

    #Calculamos la diferencia entre hora de detección de error y hora de envío de slack
    data['diferencia'] = data['slackSendTime'] - data['errorDetectionTime']
    data['diferencia_segundos'] = data['diferencia'].dt.total_seconds()

    #Quitamos la columna de diferencia
    data = data.drop(['diferencia'], axis = 1)

    #Ordenamos de manera ascendente por el requestTime
    data = data.sort_values(by = 'requestTime', ascending = True)

    #Quitamos zonahoraria en columnas de fecha
    cols_fechas = ['requestTime', 'slackSendTime', 'errorDetectionTime']

    for col in cols_fechas:
        data[col] = data[col].dt.tz_localize(None)

    #Extraemos la hora de la fecha
    data['hora_request'] = data['requestTime'].dt.strftime('%H:%M:%S')

    #Cambiamos el valor de isAvailabel
    data['isAvailable'] = list(map(lambda x: 0 if x is True else 1, data['isAvailable']))

    #Reorganizamos dataframe
    data = data[['id', 'requestTime', 'statusCode', 'errorDetectionTime', 'slackSendTime', 'status', 
                 'created', 'updated', 'isAvailable', 'hora_request', 'diferencia_segundos']]
    
    #Volvemos a exportar el archivo
    data.to_excel('datos_experimento.xlsx', index = False)