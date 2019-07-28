# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from price_monitor.models import IGA

class IGASpider(Spider):
    name = 'iga_spider'
    allowed_domains = IGA.allowed_domains
    custom_settings = IGA.custom_settings
    start_urls = [
        'https://www.iga.net/en/product/yop-yogurt-drinkraspberry/00000_000000005692001202',
        'https://www.iga.net/en/product/yop-yogurt-drinkblueberry/00000_000000005692001210',
        'https://www.iga.net/en/product/chocolate-milk1-/00000_000000005587210518',
        'https://www.iga.net/en/product/cheesemarble-cheddar/00000_000000006810090189'
    ]

    def __init__(self, *a, **kw):
        super(IGASpider, self).__init__(*a, **kw)
        self.iga = IGA()

    def parse(self, response):
        return self.iga.parse_product(response)