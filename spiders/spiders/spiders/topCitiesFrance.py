import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

DOCS_FOLDER = '../../../docs/'

# Name of the file where the results will be saved
filename = 'topCitiesFrance.json'

class TopcitiesfranceSpider(scrapy.Spider):
    name = 'topCitiesFrance'
    allowed_domains = ['one-week-in.com']
    start_urls = ['https://one-week-in.com/35-cities-to-visit-in-france/']

    def parse(self, response):
        ## we get the first <ol> element then text inside all <li> child
        cities = response.xpath("(//ol)[1]//li/a//text()").getall()
        yield {
            'cities': cities
        }
'''
If file already exists, delete it before crawling (because Scrapy will 
concatenate the last and new results otherwise)
'''

if filename in os.listdir(DOCS_FOLDER):
        os.remove(DOCS_FOLDER + filename)

process = CrawlerProcess(settings = {
    'USER_AGENT': 'Chrome/97.0',
    'LOG_LEVEL': logging.INFO,
    'FEED_EXPORT_ENCODING': 'utf-8',
    "FEEDS": {
        DOCS_FOLDER + filename : {"format": "json"},
    }
})

process.crawl(TopcitiesfranceSpider)
process.start()