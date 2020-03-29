from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models.incase import Incase

class IncaseSpider(Spider):
    name = 'incase_spider'
    allowed_domains = Incase.allowed_domains
    custom_settings = Incase.custom_settings
    start_urls = [
        'https://incasedesigns.ca/products/cl55532-blk-os',
    ]

    def __init__(self, *a, **kw):
        super(IncaseSpider, self).__init__(*a, **kw)
        self.incase = Incase()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta={'js_global_variable': 'window.productJSON'})

    def parse(self, response):
        return self.incase.parse_product(response)