from typing import Generator

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By

from testcase.items import TestcaseItem


class AuthosSpider(scrapy.Spider):
    name = "authos"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.driver = webdriver.Chrome()
    
    def close(self, reason: str):
        self.driver.close()
        return self.close(reason)

    def parse(self, response: Response, **kwargs):
        for auto in response.css(".address::attr(href)").getall():
            auto_detail_url = response.urljoin(auto)
            yield response.follow(auto_detail_url, callback=self.parse_auto)
        
        next_page = response.css(".js-next::attr(href)")
        if next_page != "javascript:void(0)":
            yield response.follow(next_page, callback=self.parse)
    

    def _parse_phone_number(self, response: Response, product: scrapy.Selector):
        absolute_url = response.urljoin(product.css(".address::attr(href)").get())
        self.driver.get(absolute_url)
        show = self.driver.find_element(By.CLASS_NAME, "phone_show_link")
        show.click()

    def parse_auto(self, response: Response) -> Generator:
        url = response.url
        title = response.css(".auto_content_title::text").get()
        price_usd = int(response.css(".price_value::text").get().lstrip("$"))
        odometr = int(response
                      .css(".m-pading .bold.dhide::text")
                      .get()
                      .lstrip("тис. км пробіг"))
        username = response.css(".seller_info_name_bold a::text").get()
        phone_number = self._parse_phone_number(response=response)
        image_url = response.css(".carousel-iner source::attr(srcset)").get()
        image_count = int(response.css(".count_photo .dhide::text").get().strip("з"))
        car_number = response.css(".state-num::text").get()
        car_vin = response.css(".label-vin::text").get()

        auto = TestcaseItem(
            url,
            title,
            price_usd,
            odometr,
            username,
            phone_number,
            image_count,
            image_url,
            car_number,
            car_vin
        )
    
        yield auto
