from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models.the_brick import TheBrick

class TheBrickSpider(Spider):
    name = 'the_brick_spider'
    allowed_domains = TheBrick.allowed_domains
    custom_settings = TheBrick.custom_settings
    start_urls = [
        'https://www.thebrick.com/products/sony-65-x950g-4k-uhd-led-smart-television-xbr65x950g#cm-store',
    ]

    def __init__(self, *a, **kw):
        super(TheBrickSpider, self).__init__(*a, **kw)
        self.the_brick = TheBrick()

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, dont_filter=True, meta={'js_global_variable': 'window.Shopify'})

    def parse(self, response):
        return self.the_brick.parse_product(response)