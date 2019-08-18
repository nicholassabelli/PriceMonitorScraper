# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spiders import Spider
from price_monitor.models.best_besy import BestBuy

class BestBuySpider(Spider):
    name = 'best_buy_spider'
    allowed_domains = BestBuy.allowed_domains
    custom_settings = BestBuy.custom_settings
    start_urls = [
        # 'https://www.bestbuy.ca/en-ca/product/sony-65-4k-uhd-hdr-led-android-smart-tv-xbr65x950g/13375799',
        # 'https://www.bestbuy.ca/en-ca/product/spider-man-ps4/10439890.aspx',
        # 'https://www.bestbuy.ca/en-ca/product/apple-macbook-pro-with-touch-bar-13-3-space-grey-intel-core-i5-2-3ghz-256gb-8gb-ram-english/12727808.aspx?',
        'https://www.bestbuy.ca/en-ca/product/marvel-ultimate-alliance-3-the-black-order-switch/13367461',
        'https://www.bestbuy.ca/fr-ca/produit/marvel-ultimate-alliance-3-the-black-order-switch/13367461',
        # 'https://www.bestbuy.ca/en-ca/product/star-wars-jedi-fallen-order-ps4/12601493',
        # 'https://www.bestbuy.ca/en-ca/product/lego-star-wars-moloch-s-landspeeder-464-pieces-45210/12293487',
        # 'https://www.bestbuy.ca/en-ca/product/lego-star-wars-darth-vader-transformation-282-pieces-75183/11264410',
        # 'https://www.bestbuy.ca/en-ca/product/incomm-sony-playstation-3-50-prepaid-card-n-a/10123760',
        # 'https://www.bestbuy.ca/en-ca/product/lego-star-wars-the-force-awakens-ps3/12482031',
    ]

    def __init__(self, *a, **kw):
        super(BestBuySpider, self).__init__(*a, **kw)
        self.best_buy = BestBuy()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta={'js_global_variable': 'window.data_layer'})

    def parse(self, response):
        return self.best_buy.parse_product(response)


# 75x75
# twobyone > div.at-total-container > div:nth-child(1) > img

# 500x500
# #pagecontent > div > div.prod-detail-wrapper.jmvc-controller-pdp.ng-scope.pdp_desktop.pdp_ui > div > div.prod-detail-bot > div > div.prod-detail-assets.span7 > div.core-utilities > div > div:nth-child(2) > div > div.gallery-image-container > div > div:nth-child(2) > img