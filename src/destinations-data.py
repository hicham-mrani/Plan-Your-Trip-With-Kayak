import requests as req
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path

#personnal lib
from my_functions import export_csv, export_json

# CONSTANTS
DOCS_FOLDER = '../docs/'
POLYGONS = '../docs/polygons/'
FILENAME = 'topCitiesFrance.json'
ENDPOINT =  'https://nominatim.openstreetmap.org/'
SEARCH = ENDPOINT + 'search'

def get_cities_infos(cities:list)->list:
    cities_infos = []
    polygons = []
    if cities:
        for city in cities:
            try:
                # we test if we recover the result at index 0 of our answer for the city request
                response = req.get(SEARCH, params={'city': city, 'country':'france', 'format':'json', 'polygon_geojson': 1}).json()[0]
            except IndexError: 
                # if we have an exception, we test if we recover the result at index 0 of our answer for the street request
                try:
                    response = req.get(SEARCH, params={'street': city, 'country':'france', 'format':'json', 'polygon_geojson': 1}).json()[0]
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
                export_json(dictionary=response["geojson"], rel_path=os.path.join(POLYGONS,'france/'), file_name = city_name)
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
        with open(DOCS_FOLDER + FILENAME, encoding='utf-8') as file:
            contents = json.load(file)[0]['cities']
        file.close()
    except NameError as err:
        print(err)
    except FileNotFoundError as err:
        print("File Not Found")
    else:
        cities = contents

    data_cities = get_cities_infos(cities)
    export_csv(data = data_cities, rel_path = DOCS_FOLDER, file_name = 'cities_infos.csv')

    
main()

