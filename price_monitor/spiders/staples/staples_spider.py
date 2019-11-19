# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from price_monitor.models.staples import Staples

class StaplesSpider(Spider):
    name = 'staples_spider'
    allowed_domains = Staples.allowed_domains
    custom_settings = Staples.custom_settings
    start_urls = [
        'https://www.bestbuy.ca/en-ca/product/spider-man-ps4/10439890.aspx',
    ]

    def __init__(self, *a, **kw):
        super(StaplesSpider, self).__init__(*a, **kw)
        self.staples = Staples()

    def parse(self, response):
        return self.staples.parse_product(response)