# -*- coding: utf-8 -*-

import logging, datetime, json
from price_monitor.items import Offer, Product
from price_monitor.item_loaders import OfferItemLoader, IGAProductItemLoader
from price_monitor.models import Currency

class Walmart:
    store_name = 'Walmart'
    domain = 'walmart.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.StripAmountPipeline': 300,
            # 'price_monitor.pipelines.BreadcrumbTagsPipeline': 800,
            # 'price_monitor.pipelines.IGAUniversalProductCodePipeline': 900,
            'price_monitor.pipelines.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def parse_product(self, response):
        sku = None
        entities = None
        product = None
        js_data = response.meta.get('js_data')

        product_data = response.css('div.js-content div.css-ay2u5v.evlleax1 script::text').get()

        if product_data:
            product_data = json.loads(product_data)
            # logging.info('product_data')
            # logging.info(product_data['offers'])

        if product_data:
            offers = product_data.get('offers')

        if js_data:
            entities = js_data.get('entities')
            product = js_data.get('product')

        if product and product.get('activeSkuId'):
            sku = product['activeSkuId']

        productLoader = IGAProductItemLoader(response=response)
        productLoader.add_value(Product.KEY_STORE, [self.store_name])
        productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_value(Product.KEY_URL, [response.url])
        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price(response, product_data)])

        productLoader.add_css(Product.KEY_SOLD_BY, ['#product-desc p.seller-info span', 'div.css-9wd9vm.etlm3820 svg title', 'div.css-9wd9vm.etlm3820 a.css-1syn49.elkyjhv0'])

        # Description
        if sku and entities and entities.get('skus').get(sku).get('description'):
            productLoader.add_css(Product.KEY_NAME, ['#product-desc h1', 'div.css-13hwhay.e1yn5b3f0 h1'])
        elif product and product.get('item').get('description'):
            productLoader.add_css(Product.KEY_NAME, ['#product-desc h1', 'div.css-13hwhay.e1yn5b3f0 h1'])
        else:
            productLoader.add_css(Product.KEY_NAME, ['#product-desc h1', 'div.css-13hwhay.e1yn5b3f0 h1'])

        # Brand
        if sku and entities.get('skus').get(sku).get('brand').get('name'):
            productLoader.add_css(Product.KEY_BRAND, ['#product-desc p.brand a.brand-link', 'div.css-uxtmi3.e1yn5b3f4 span a.css-1syn49.elkyjhv0'])
        else:
            productLoader.add_css(Product.KEY_BRAND, ['#product-desc p.brand a.brand-link', 'div.css-uxtmi3.e1yn5b3f4 span a.css-1syn49.elkyjhv0'])

        # productLoader.add_xpath(Product.KEY_TAGS, ['//ul[contains(concat(" ", normalize-space(@class), " "), " breadcrumb ")]/li[last()-1]/a/@href'])
        # productLoader.add_value(Product.KEY_UPC, [response.url])
        return productLoader.load_item()

    def __get_price(self, response, offers):
        priceLoader = OfferItemLoader(response=response)

        if offers and offers.get('price'):
            priceLoader.add_value(Offer.KEY_AMOUNT, str(offers.get('price')))
        else:
            priceLoader.add_css(Offer.KEY_AMOUNT, ['span[itemprop=price]', 'div.css-k008qs.e1ufqjyx0 > span.css-rykmet.esdkp3p2 > span.css-2vqe5n.esdkp3p0', 'body > div.js-content > div:nth-child(1) > div > div > div.css-0.eewy8oa0 > div.css-1i2cfe3.eewy8oa2 > div.css-18f77yw.eewy8oa4 > div > div.css-0.e1cd9jig0 > div > div.css-mzzkn5.e1yn5b3f5 > div > div > div.css-k008qs.e1ufqjyx0 > span.css-rykmet.esdkp3p2 > span'])

        if offers and offers.get('priceCurrency'):
            priceLoader.add_value(Offer.KEY_CURRENCY, offers.get('priceCurrency'))
        else:
            priceLoader.add_value(Offer.KEY_CURRENCY, [Currency.CAD.value])

        priceLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(priceLoader.load_item())
