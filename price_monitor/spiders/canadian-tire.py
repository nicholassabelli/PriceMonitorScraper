# -*- coding: utf-8 -*-

import scrapy
import logging

class CantireSpider(scrapy.spiders.SitemapSpider):
    name = 'cantire'
    allowed_domains = ['canadiantire.ca']
    sitemap_urls = ['http://canadiantire.ca/robots.txt']

    def parse(self, response):
        logging.info(response.url)
