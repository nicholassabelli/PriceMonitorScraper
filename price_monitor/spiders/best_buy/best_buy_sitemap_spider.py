from scrapy.spiders import SitemapSpider
from price_monitor.models.best_besy import BestBuy

class BestBuySitemapSpider(SitemapSpider):
    name = 'best_buy_sitemap_spider'
    allowed_domains = BestBuy.allowed_domains
    custom_settings = BestBuy.custom_settings
    sitemap_urls = ['http://www.bestbuy.ca/robots.txt']
    sitemap_rules = [
        ('/en-ca/product/', 'parse_product'),
    ]

    def __init__(self, *a, **kw):
        super(BestBuySitemapSpider, self).__init__(*a, **kw)
        self.best_buy = BestBuy()

    def parse_product(self, response):
        return self.best_buy.parse_product(response)

