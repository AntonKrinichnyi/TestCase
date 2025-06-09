from pathlib import Path

import scrapy
from scrapy.http import Response


class AuthosSpider(scrapy.Spider):
    name = "authos"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    def parse(self, response: Response, **kwargs):
        for auto in response.css(".address::attr(href)"):
            yield {"url": auto}
