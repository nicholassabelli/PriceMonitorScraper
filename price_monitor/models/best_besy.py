# -*- coding: utf-8 -*-

import datetime, logging, json, re
from price_monitor.items import Offer, Product
from price_monitor.item_loaders import OfferItemLoader, ProductItemLoader
from price_monitor.models import Currency

class BestBuy:
    store_name = 'Best Buy'
    sold_by = 'Best Buy Canada Ltd.'
    domain = 'bestbuy.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.TagsPipeline': 300,
        }
    }

    def parse_product(self, response):
        data = None
        texts = response.xpath('//script/text()')

        for text in texts:
            match = text.re(".*window.__INITIAL_STATE__.*")

            if match:
                text = match[0].strip().split('window.__INITIAL_STATE__ = ')[1]

                if text.endswith(';'):
                    text = text[:-1]
                
                data = json.loads(text)
        
        if data:
            # f = open("bbproduct.json", "w")
            # f.write(json.dumps(data))
            # f.close()
            return self.__load_with_dictionary(response, data)

        productLoader = ProductItemLoader(response=response)
        productLoader.add_value(Product.KEY_STORE, [self.store_name])
        productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_css(Product.KEY_NAME, ['div.x-product-detail-page > h1[itemprop="name"]'])
        productLoader.add_css(Product.KEY_DESCRIPTION, ['head > meta[name="description"]::attr(content)'])
        # productLoader.add_css(Product.KEY_RELEASE_DATE, ['#ctl00_CP_ctl00_PD_lblReleaseDate'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        # productLoader.add_css(Product.KEY_AVAILABILITY, ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > link[itemprop="availability"]::attr(href)'])
        # productLoader.add_css(Product.KEY_TAGS, ['head > meta[name="keywords"]::attr(content)'])
        # # productLoader.add_css('brand', ['div[data-brand-bar]::attr(data-brand-bar)'])
        # # productLoader.add_value('brand', [brand])
        return productLoader.load_item()

    def __get_price(self, response):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_css(Offer.KEY_AMOUNT, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="price"]::attr(content)'])
        priceLoader.add_css(Offer.KEY_CURRENCY, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="priceCurrency"]::attr(content)'])
        priceLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(priceLoader.load_item())

    def __get_price_with_dictionary(self, response, data):
        priceLoader = OfferItemLoader(response=response)
        priceLoader.add_value(Offer.KEY_AMOUNT, data['priceWithoutEhf'])
        priceLoader.add_value(Offer.KEY_CURRENCY, Currency.CAD)
        priceLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(priceLoader.load_item())

    def __load_with_dictionary(self, response, data):
        # logging.info('__loadWithDictionary')
        productLoader = ProductItemLoader(response=response)

        if not data or not data.get('product').get('product'):
            return productLoader.load_item()

        product = data['product']['product']

        # TODO: Verify product.
        # logging.info(product)

        productLoader.add_value(Product.KEY_STORE, [self.store_name])
        productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_value(Product.KEY_NAME, product['name'])
        productLoader.add_css(Product.KEY_DESCRIPTION, ['head > meta[name="description"]::attr(content)'])
        productLoader.add_value(Product.KEY_RELEASE_DATE, product['preorderReleaseDate'])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response)])
        productLoader.add_value(Product.KEY_URL, [response.url])
        # productLoader.add_value(Product.KEY_AVAILABILITY, )
        # productLoader.add_css(Product.KEY_TAGS, ['head > meta[name="keywords"]::attr(content)'])
        productLoader.add_value(Product.KEY_BRAND, product['brandName'])
        return productLoader.load_item()
