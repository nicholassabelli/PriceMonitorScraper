# -*- coding: utf-8 -*-

import logging
from scrapy.spiders import SitemapSpider

class CantireSpider(SitemapSpider):
    name = 'cantire'
    allowed_domains = ['canadiantire.ca']
    sitemap_urls = ['http://canadiantire.ca/robots.txt']

    def parse(self, response):
        logging.info(response.url)
