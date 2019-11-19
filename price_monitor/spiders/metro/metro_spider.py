# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from price_monitor.models.metro import Metro

class MetroSpider(Spider):
    name = 'metro_spider'
    allowed_domains = Metro.allowed_domains
    custom_settings = Metro.custom_settings
    start_urls = [
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/yogurt/drinkable-yogurts/2-raspberry-flavoured-drinkable-yogurt/p/056920012029',
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/flavoured-milk/1-chocolate-milk/p/068700106361',
        'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/1-skim-milk/1-milk/p/055872700114',
    ]

    def __init__(self, *a, **kw):
        super(MetroSpider, self).__init__(*a, **kw)
        self.metro = Metro()

    def parse(self, response):
        return self.metro.parse_product(response)