import scrapy
import re
from ..items import ShopSpiderItem


class EnamelSpider(scrapy.Spider):
    name = 'enamel'
    start_urls = [
        'https://krasn.russcvet.ru/catalog/enamels/'
    ]

    def price_format(self, price_raw):
        pattern = r'\d+'
        price = re.findall(pattern=pattern, string=price_raw)
        try:
            return price[0]
        except IndexError:
            return price_raw.strip('"').strip(' ')

    def parse(self, response, **kwargs):
        for item in response.css('div.catalog-item'):
            output = ShopSpiderItem()
            price_raw = item.css('span.catalog-item-price::text').get()
            price = self.price_format(price_raw)

            output['name'] = item.css('div.name a::text').get()
            output['price'] = price

            yield output

        next_page = response.css('a.modern-page-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
