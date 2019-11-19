from scrapy.spiders import SitemapSpider
from price_monitor.models.iga import IGA

class IGASitemapSpider(SitemapSpider):
    name = 'iga_sitemap_spider'
    allowed_domains = IGA.allowed_domains
    custom_settings = IGA.custom_settings
    sitemap_urls = ['http://www.iga.net/robots.txt']
    sitemap_rules = [
        ('/en/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(IGASitemapSpider, self).__init__(*a, **kw)
        self.iga = IGA()

    def parse_product(self, response):
        return self.iga.parse_product(response)