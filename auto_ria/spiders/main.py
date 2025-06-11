import time
from typing import Generator
import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from auto_ria.items import AutoRiaItem

class AuthosSpider(scrapy.Spider):
    name = "autos"
    allowed_domains = ["auto.ria.com"]
    start_urls = [
        "https://auto.ria.com/uk/search/?indexName=auto&brand.id[0]=48&model.id[0]=425&year[0].gte=2015&categories.main.id=1&price.currency=1&abroad.not=0&custom.not=1&size=50&body.id[0]=3"
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.driver = webdriver.Chrome()

    def close_spider(self, reason):
        if hasattr(self, "driver"):
            self.driver.quit()
        super().close_spider(reason)

    def parse(self, response: Response):
        urls = response.css(".ticket-item .content-bar a.m-link-ticket::attr(href)").getall()
        self.logger.info(f"Found {len(urls)} URLs on page")
        for item in urls:
            if item:
                yield response.follow(item, callback=self.parse_auto)
        
        self.driver.get(response.url)
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        next_page = self.driver.find_element(By.XPATH, '//a[contains(@class, "page-link") and contains(text(), "Вперед")]')
        last_page = self.driver.find_element(By.XPATH, '//a[contains(@class, "page-link disabled")" and contains(text(), "Вперед")]')
        if next_page and not last_page:
            yield next_page.click()

    def _parse_phone_number(self, response: Response) -> str:
        self.driver.get(response.url)
        time.sleep(2)
        self.driver.execute_script("window.scrollBy(0,400)")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="phonesBlock"]/div/span/span')
                )
            ).click()
        except Exception as e:
            print(e)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="react-phones"]/div[1]/span/span[1]')
                    )
                ).click()
            except Exception as e:
                print(e)

        time.sleep(1)
        try:
            phone_number = self.driver.find_element(
                By.XPATH, '//*[@id="openCallMeBack"]/div[2]/div[2]'
            ).text
        except Exception as e:
            print(e)
            try:
                phone_number = self.driver.find_element(
                    By.XPATH, "/html/body/section/div[1]/div[2]/div/section/div[5]/a"
                ).text
            except Exception as e:
                phone_number = None
                print("Number is not valid or not exist")
        return phone_number

    def parse_auto(self, response: Response) -> Generator:
        url = response.url
        title = response.css(".auto_content_title::text").get()
        price = response.css(".price_value strong::text").get()
        price_usd = int(price.replace(" ", "").strip("$")) if price else None
        odometr = response.css(".auto-wrap .size18::text").get()
        odometr = int(odometr) * 1000 if odometr else None
        username = response.css(".seller_info_name_bold a::text").get()
        phone_number = self._parse_phone_number(response=response)
        image_url = response.css(".carousel-iner source::attr(srcset)").get()
        image_count_text = response.css(".count_photo .dhide::text").get()
        image_count = int(image_count_text.strip("з")) if image_count_text else 0
        car_number = response.css(".state-num::text").get()
        car_vin = response.css(".label-vin::text").get()

        try:
            auto = AutoRiaItem(
                url=url,
                title=title,
                price_usd=price_usd,
                odometr=odometr,
                username=username,
                phone_number=phone_number,
                image_count=image_count,
                image_url=image_url,
                car_number=car_number,
                car_vin=car_vin,
            )
            yield auto
        except Exception as e:
            self.logger.error(f"Error {response.url}: {str(e)}")
