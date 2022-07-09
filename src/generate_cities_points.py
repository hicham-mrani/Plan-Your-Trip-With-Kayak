# LIBRARIES
import os
import json
import requests
import pandas as pd
import numpy as np
from pathlib import Path
from my_functions import export_json # private module

# CONSTANTS
DOCS = '../docs/'
GEOJSON = '../docs/geojson/'
API_NOMINATIM =  'https://nominatim.openstreetmap.org/'
FILENAME = 'topCitiesFrance.json'

# FUNCTIONS
def get_cities_infos(cities:list)->list:
    cities_infos = []
    if cities:
        for city in cities:
            try:
                # we test if we recover the result at index 0 of our answer for the city request
                response = requests.get(API_NOMINATIM + 'search', params={'city': city, 'country':'france', 'format':'json', 'polygon_geojson': 1}).json()[0]
            except IndexError: 
                # if we have an exception, we test if we recover the result at index 0 of our answer for the street request
                try:
                    response = requests.get(API_NOMINATIM + 'search', params={'street': city, 'country':'france', 'format':'json', 'polygon_geojson': 1}).json()[0]
                except IndexError:
                    # if we have an exception again, so we pass and set the city gps as ""
                    response = False
                    pass
            if response:
                city_name = response["display_name"].split(',')[0]

                cities_infos.append({
                    "city_name": city_name,
                    "lat": response["lat"],
                    "lon": response["lon"],
                    })
            else:
                cities_infos.append({
                    "city_name": city,
                    "lat": "",
                    "lon": "",
                    })
    return cities_infos
    
def main():
    cities = []

    # Get cities list from topCitiesFrance.json
    try:
        with open(DOCS + FILENAME, encoding='utf-8') as file:
            contents = json.load(file)[0]['cities']
        file.close()
    except NameError as err:
        print(err)
    except FileNotFoundError as err:
        print("File Not Found")
    else:
        cities = contents

    data_cities = get_cities_infos(cities)

    df = pd.DataFrame(data=data_cities)
    df.to_csv(DOCS+'cities_points.csv', index=False)

# MAIN
main()

