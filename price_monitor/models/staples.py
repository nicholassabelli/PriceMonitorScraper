# -*- coding: utf-8 -*-

from price_monitor.item_loaders import OfferItemLoader, ProductItemLoader

class Staples:
    allowed_domains = ['staples.ca']
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.TagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        productLoader = ProductItemLoader(response=response)
        productLoader.add_css('name', ['head > meta[property="og:title"]::attr(content)'])
        productLoader.add_css('description', ['head > meta[name="description"]::attr(content)'])
        productLoader.add_css('releaseDate', ['#ctl00_CP_ctl00_PD_lblReleaseDate'])
        productLoader.add_value('currentPrice', [self.__get_price(response)])
        productLoader.add_value('url', [response.url])
        productLoader.add_css('availability', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > link[itemprop="availability"]::attr(href)'])
        productLoader.add_css('tags', ['head > meta[name="keywords"]::attr(content)'])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_css('amount', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="price"]::attr(content)'])
        priceLoader.add_css('currency', ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > meta[itemprop="priceCurrency"]::attr(content)'])
        return dict(priceLoader.load_item())