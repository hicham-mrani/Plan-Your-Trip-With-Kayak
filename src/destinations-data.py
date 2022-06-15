import requests as req
import json
import pandas as pd

# CONSTANTS
DOCS_FOLDER = '../docs/'
FILENAME = 'topCitiesFrance.json'
ENDPOINT =  'https://nominatim.openstreetmap.org/'
SEARCH = ENDPOINT + 'search'

def get_cities_infos(cities:list)->list:
    cities_infos = []
    if cities:
        for city in cities:
            try:
                response = req.get(SEARCH, params={'city': city, 'country':'france', 'format':'json'}).json()[0]
            except IndexError: 
                response = req.get(SEARCH, params={'street': city, 'country':'france', 'format':'json'}).json()[0]
            else:
                cities_infos.append({
                    'name': response['display_name'].split(',')[0],
                    'lat': response['lat'],
                    'lon': response['lon']
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

    get_cities_infos(cities)

main()

