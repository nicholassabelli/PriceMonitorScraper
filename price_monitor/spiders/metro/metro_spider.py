# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from price_monitor.models.metro import Metro

class MetroSpider(Spider):
    name = 'metro_spider'
    allowed_domains = Metro.allowed_domains
    custom_settings = Metro.custom_settings
    start_urls = [
        # 'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/yogurt/drinkable-yogurts/2-raspberry-flavoured-drinkable-yogurt/p/056920012029',
        # 'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/flavoured-milk/1-chocolate-milk/p/068700106361',
        # 'https://www.metro.ca/en/online-grocery/aisles/dairy-cheese/milk-cream/1-skim-milk/1-milk/p/055872700114',
        # 'https://www.metro.ca/en/online-grocery/aisles/dairy-eggs/milk-cream-butter/flavoured-milk/1-chocolate-milk/p/055872094015',
        # 'https://www.metro.ca/en/online-grocery/aisles/beer-wine/beer-cider/classic-beer/lager-beer/p/056327702547',
        'https://www.metro.ca/epicerie-en-ligne/allees/bieres-et-vins/bieres-et-cidres/bieres-classiques/biere-de-type-lager/p/056327702547',
    ]

    # TODO: Make sure only certain urls work with the spider. Also needs to work with the decision to use this spider given a URL.

    def __init__(self, *a, **kw):
        super(MetroSpider, self).__init__(*a, **kw)
        self.metro = Metro()

    def parse(self, response):
        return self.metro.parse_product(response)