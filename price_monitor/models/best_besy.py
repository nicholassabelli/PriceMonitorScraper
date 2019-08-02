# -*- coding: utf-8 -*-

import datetime, logging, json, re
from price_monitor.items import Offer, Product, Store
from price_monitor.item_loaders import OfferItemLoader, ProductItemLoader, StoreItemLoader
from price_monitor.models import Availability, Condition, Currency, Region, UniversalProductCode

class BestBuy:
    store_id = 'best_buy_canada' # TODO: Constants.
    store_name = 'Best Buy'
    sold_by = 'Best Buy Canada Ltd.'
    region = Region.CANADA.value
    domain = 'bestbuy.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.StripAmountPipeline': 300,
            # 'price_monitor.pipelines.TagsPipeline': 300,
            'price_monitor.pipelines.MongoDBPipeline': 1000
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

    def __load_with_dictionary(self, response, data):
        # logging.info('__loadWithDictionary')
        productLoader = ProductItemLoader(response=response)

        if not data or not data.get('product').get('product'):
            return productLoader.load_item()

        # TODO: Verify product.
        # logging.info(product)
        # product = data['product']
        productDetails = data['product']['product']

        # productLoader.add_value(Product.KEY_STORE, [self.store_name])
        # productLoader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        # productLoader.add_value(Product.KEY_DOMAIN, [self.domain])
        productLoader.add_value(Product.KEY_URL, response.url)
        productLoader.add_value(Product.KEY_NAME, productDetails['name'])
        productLoader.add_value(Product.KEY_DESCRIPTION, productDetails['shortDescription'])
        # productLoader.add_css(Product.KEY_DESCRIPTION, ['head > meta[name="description"]::attr(content)'])

        # TODO: French format.
        if productDetails['preorderReleaseDate']:
            try:
                productLoader.add_value(Product.KEY_RELEASE_DATE, datetime.datetime.strptime(productDetails['preorderReleaseDate'], '%Y-%m-%d %I:%M:%S %p').replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
            except:
                try: 
                    productLoader.add_value(Product.KEY_RELEASE_DATE, datetime.datetime.strptime(productDetails['preorderReleaseDate'], '%Y-%m-%d %H:%M:%S').replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
                except:
                    raise
        # date_dt3 = datetime.strptime(productDetails['preorderReleaseDate'], '%Y-%m-%d').isoformat()

        model_number = productDetails['modelNumber']

        try:
            upc = (UniversalProductCode(model_number)).value
        except:
            upc = None

        productLoader.add_value(Product.KEY_CURRENT_PRICE, [self.__get_price_with_dictionary(response, data)])
        productLoader.add_value(Product.KEY_STORE, [self.__get_store_with_dictionary(response, data)])
        productLoader.add_value(Product.KEY_BRAND, productDetails['brandName'])
        productLoader.add_value(Product.KEY_SKU, productDetails['sku'])
        productLoader.add_value(Product.KEY_MODEL_NUMBER, model_number)
        productLoader.add_value(Product.KEY_UPC, upc)

        # productLoader.add_value(Product.KEY_AVAILABILITY, )
        # productLoader.add_css(Product.KEY_TAGS, ['head > meta[name="keywords"]::attr(content)'])
        
        return productLoader.load_item()

    def __get_price(self, response):
        offerLoader = OfferItemLoader(response=response)
        offerLoader.add_css(Offer.KEY_AMOUNT, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="price"]::attr(content)'])
        offerLoader.add_css(Offer.KEY_CURRENCY, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="priceCurrency"]::attr(content)'])
        offerLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(offerLoader.load_item())

    def __get_price_with_dictionary(self, response, data):
        offerLoader = OfferItemLoader(response=response)

        if not data or not data.get('product').get('product'):
            return offerLoader.load_item()

        product = data['product']
        productDetails = data['product']['product']

        offerLoader.add_value(Offer.KEY_AMOUNT, str(productDetails['priceWithoutEhf']))
        offerLoader.add_value(Offer.KEY_AVAILABILITY, self.__get_availability_with_dictionary(product))
        offerLoader.add_value(Offer.KEY_CURRENCY, Currency.CAD.value)
        offerLoader.add_value(Offer.KEY_CONDITION, Condition.NEW.value)
        offerLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        offerLoader.add_value(Offer.KEY_SKU, productDetails['sku'])
        offerLoader.add_value(Offer.KEY_SOLD_BY, [self.sold_by])
        offerLoader.add_value(Offer.KEY_STORE_ID, [self.store_id])

        return dict(offerLoader.load_item())

    def __get_store_with_dictionary(self, response, data):
        storeLoader = StoreItemLoader(response=response)

        # if not data or not data.get('product').get('product'):
        #     return storeLoader.load_item()

        # product = data['product']
        # productDetails = data['product']['product']

        storeLoader.add_value(Store.KEY_DOMAIN, [self.domain])
        storeLoader.add_value(Store.KEY_ID, [self.store_id])
        storeLoader.add_value(Store.KEY_NAME, [self.store_name])
        storeLoader.add_value(Store.KEY_REGION, self.region)
        return dict(storeLoader.load_item())

    def __get_availability_with_dictionary(self, product):
        productDetails = product['product']
        # is_online_only = productDetails['isOnlineOnly']
        is_preorderable = productDetails['isPreorderable']
        # pickup_purchasable = product['availability']['pickup']['purchasable']
        shipping_purchasable = product['availability']['shipping']['purchasable']
        is_in_store_only = True if product['availability']['shipping']['status'] == Availability.IN_STORE_ONLY.value else False

        availability = Availability.UNKNOWN.value

        if is_preorderable:
            availability = Availability.PREORDER.value
        elif is_in_store_only:
            availability = Availability.IN_STORE_ONLY.value
        elif not is_preorderable and not is_in_store_only and shipping_purchasable: #(is_online_only and not pickup_purchasable and shipping_purchasable) or 
            availability = Availability.IN_STOCK.value
        elif not shipping_purchasable:
            availability = Availability.OUT_OF_STOCK.value

        return availability