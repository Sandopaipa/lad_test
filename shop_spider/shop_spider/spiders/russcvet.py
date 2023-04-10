import scrapy
import re
from ..items import ShopSpiderItem

class EnamelSpider(scrapy.Spider):
    name = 'enamel'
    start_urls = [
        'https://krasn.russcvet.ru/catalog/enamels/'
    ]

    def parse(self, response, **kwargs):
        for item in response.css('div.catalog-item'):
            output = ShopSpiderItem()
            price_raw = item.css('span.catalog-item-price::text').get()
            price = re.findall(pattern=r'\d+', string=price_raw)

            output['name'] = item.css('div.name a::text').get()
            output['price'] = price[0]

            yield output