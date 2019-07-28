# -*- coding: utf-8 -*-

from price_monitor.item_loaders import OfferItemLoader, ProductItemLoader

class TheSource:
    allowed_domains = ['thesource.ca']
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.TagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        productLoader = ProductItemLoader(response=response)
        productLoader.add_css('name', ['title'])
        productLoader.add_css('description', ['head > meta[name="description"]::attr(content)'])
        productLoader.add_value('currentPrice', [self.__get_price(response)])
        productLoader.add_value('url', [response.url])
        productLoader.add_css('availability', ['div.availability-text::attr(content)'])
        productLoader.add_css('tags', ['head > meta[name="keywords"]::attr(content)'])
        productLoader.add_css('upc', ['div.product-details-numbers-wrapper > div:nth-child(2)'])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_css('amount', ['#addToCartForm > input[name="price"]::attr(value)'])
        priceLoader.add_css('currency', ['section.pdp-section > meta[itemprop="priceCurrency"]::attr(content)'])
        return dict(priceLoader.load_item())