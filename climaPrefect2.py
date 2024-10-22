from prefect import task, flow
from datetime import datetime, timedelta as td
import requests

# Definimos la tarea para obtener el pronóstico del clima
@task(retries=2)
def get_weather_forecast():
    API_KEY = 'd43aa1911a778b5153f858367ede330e'
    BASE_URL = 'http://api.openweathermap.org/data/2.5/forecast'
    city = 'San Miguel de Tucuman'

    params = {
        'q': city,
        'APPID': API_KEY,
        'units': 'metric',
        'lang': 'es'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        tomorrow = datetime.now() + td(days=1)
        tomorrow_noon = tomorrow.replace(hour=12, minute=0, second=0, microsecond=0)
        tomorrow_str = tomorrow_noon.strftime("%d-%m-%Y")
        
        forecast = None
        for entry in data['list']:
            forecast_time = datetime.fromtimestamp(entry['dt'])
            if forecast_time.date() == tomorrow_noon.date() and forecast_time.hour == 12:
                forecast = entry
                break
        
        if forecast:
            main = forecast['main']
            weather_description = forecast['weather'][0]['description']
            temp = main['temp']
            humidity = main['humidity']

            print(f"Pronóstico para {city} al mediodía de mañana ({tomorrow_str}):")
            print(f"Descripción: {weather_description.capitalize()}")
            print(f"Temperatura: {temp}°C")
            print(f"Humedad: {humidity}%")
        else:
            print(f"No se encontró un pronóstico exacto para el mediodía de mañana ({tomorrow_str}).")
    else:
        print(f"Error al obtener los datos: {response.status_code}")

# Definimos el flujo principal
@flow
def weather_forecast_flow():
    get_weather_forecast()

if __name__ == "__main__":
    weather_forecast_flow()
