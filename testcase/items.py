# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestcaseItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price_usd = scrapy.Field()
    odometr = scrapy.Field()
    username = scrapy.Field()
    phone_number = scrapy.Field()
    image_url = scrapy.Field()
    image_count = scrapy.Field()
    car_number = scrapy.Field()
    car_vin = scrapy.Field()
