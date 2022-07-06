# LIBRARIES
import os
import sys
import requests as req
import pandas as pd
from datetime import datetime
from my_utils import EnvironmentVariables # private module
from my_functions import export_csv # private module

env_manager = EnvironmentVariables() # class instance

# CONSTANTS
DOCS = '../docs/'
API_OWM = 'https://api.openweathermap.org'
API_KEY_NAME = 'FREE_OWM_API_KEY'
API_KEY_OWM = env_manager.get_value(API_KEY_NAME) # get my private key from private file on my computer
LANG = 'fr' # to get the output in french
EXCLUDE = 'hourly,minutely,current' # I just want daily weather
Unit = 'metric' # For temperature in Celsius and wind speed in meter/sec

# create dataframe of cities
cities = pd.read_csv(DOCS + 'cities_infos.csv')

# /!\ there is a paramter to provide to read_csv to avoid this line (check later)
cities.drop(columns = cities.columns[0], inplace=True) 

# get weather for all my cities from API
weather_cities = []
for city in range(len(cities)):
    response = req.get(API_OWM+'/data/2.5/onecall', params={'lat': cities['lat'][city], 'lon': cities['lon'][city],'units': Unit,'exclude': EXCLUDE, "lang": LANG, 'appid': API_KEY })
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