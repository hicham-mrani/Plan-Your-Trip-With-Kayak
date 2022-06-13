import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

JSON_FOLDER = '../../../json/'

class TopcitiesfranceSpider(scrapy.Spider):
    name = 'topCitiesFrance'
    allowed_domains = ['one-week-in.com']
    start_urls = ['https://one-week-in.com/35-cities-to-visit-in-france/']

    def parse(self, response):
        cities = response.xpath("(//ol)[1]//li/a//text()").getall()
        yield {
            'cities': cities
        }

# Name of the file where the results will be saved
filename = 'topCitiesFrance.json'

'''
If file already exists, delete it before crawling (because Scrapy will 
concatenate the last and new results otherwise)
'''

if filename in os.listdir(JSON_FOLDER):
        os.remove(JSON_FOLDER + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    'FEED_EXPORT_ENCODING': 'utf-8',
    "FEEDS": {
        JSON_FOLDER + filename : {"format": "json"},
    }
})

process.crawl(TopcitiesfranceSpider)
process.start()

with open(JSON_FOLDER + filename) as file:
    cities = json.load(file)
file.close()
