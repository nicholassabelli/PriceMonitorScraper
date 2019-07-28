# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models import Walmart

class WalmartSpider(Spider):
    name = 'walmart_spider'
    allowed_domains = Walmart.allowed_domains
    custom_settings = Walmart.custom_settings
    start_urls = [
        # 'https://www.walmart.ca/en/ip/mastro-hot-genoa-salami/6000199245768',
        # 'https://www.walmart.ca/en/ip/rogue-one-a-star-wars-story-blu-ray-dvd-digital-hd/6000196818817',
        # 'https://www.walmart.ca/en/ip/star-wars-the-black-series-6-jango-fett-action-figure/6000195359749'
        'https://www.walmart.ca/en/ip/star-wars-jedi-fallen-order-ps4/6000199891520',
        'https://www.walmart.ca/en/ip/the-legend-of-zelda-links-awakening-nintendo-switch/6000199692436'
    ]

    def __init__(self, *a, **kw):
        super(WalmartSpider, self).__init__(*a, **kw)
        self.walmart = Walmart()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta={'js_global_variable': 'window.__PRELOADED_STATE__'})

    def parse(self, response):
        return self.walmart.parse_product(response)