import os
import sys
from datetime import datetime
from my_utils import EnvironmentVariables
env_manager = EnvironmentVariables()
import requests as req
import pandas as pd

#personnal lib
from my_functions import export_csv

DOCS = '../docs/'
END_POINT = 'https://api.openweathermap.org'
API_KEY_NAME = 'FREE_OWM_API_KEY'
API_KEY = env_manager.get_value(API_KEY_NAME)
LANG = 'fr' # to get the output in french
EXCLUDE = 'hourly,minutely,current' # I just want daily weather
Unit = 'metric' # For temperature in Celsius and wind speed in meter/sec

# Get our cities list
cities = pd.read_csv(DOCS + 'cities_infos.csv')
cities.drop(columns = cities.columns[0], inplace=True)

# API call for all cities in my list
weather_cities = []
for city in range(len(cities)):
    response = req.get(END_POINT+'/data/2.5/onecall', params={'lat': cities['lat'][city], 'lon': cities['lon'][city],'units': Unit,'exclude': EXCLUDE, "lang": LANG, 'appid': API_KEY })
    data = {
        'name': cities['city_name'][city],
        'lat': cities['lat'][city],
        'lon': cities['lon'][city],
        'curr_day': response.json()['daily'][0]
    }

    for i in range(1,8):
        timestamp = response.json()['daily'][i]['dt']
        day = datetime.fromtimestamp(timestamp).strftime("%A")
        data[day] = response.json()['daily'][i]  

    weather_cities.append(data)
    
export_csv(data = weather_cities, rel_path= DOCS, file_name = 'cities_weathers.csv')