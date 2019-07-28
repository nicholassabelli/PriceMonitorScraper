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

# 75x75
# twobyone > div.at-total-container > div:nth-child(1) > img

# 500x500
# #pagecontent > div > div.prod-detail-wrapper.jmvc-controller-pdp.ng-scope.pdp_desktop.pdp_ui > div > div.prod-detail-bot > div > div.prod-detail-assets.span7 > div.core-utilities > div > div:nth-child(2) > div > div.gallery-image-container > div > div:nth-child(2) > img