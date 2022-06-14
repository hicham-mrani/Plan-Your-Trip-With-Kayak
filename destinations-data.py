import requests as req
import json
import pandas as pd

# CONSTANTS
DOCS_FOLDER = './docs/'
FILENAME = 'topCitiesFrance.json'
ENDPOINT =  'https://nominatim.openstreetmap.org/'
SEARCH = ENDPOINT + 'search'
# VARIABLES
cities = []
response = req.get(SEARCH, params={'city':'paris', 'country':'france', 'format':'json'})


# Get cities list from topCitiesFrance.json
try:
    with open(DOCS_FOLDER + FILENAME, encoding='utf-8') as file:
        contents = json.load(file)
    file.close()
except NameError as err:
    print(err)
except FileNotFoundError as err:
    print("File Not Found")
else:
    cities = contents[0]['cities']

print(response.json())