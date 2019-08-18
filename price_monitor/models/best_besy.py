# -*- coding: utf-8 -*-

import datetime, logging, json, re
from price_monitor.items import Offer, Product, ProductData, ProductDataLookup, Store
from price_monitor.item_loaders import OfferItemLoader, ProductItemLoader, ProductDataItemLoader, ProductDataLookupItemLoader, StoreItemLoader
from price_monitor.models import Availability, Condition, Currency, Language, Region, UniversalProductCode

class BestBuy:
    store_id = 'best_buy_canada' # TODO: Constants.
    store_name = 'Best Buy'
    sold_by = 'Best Buy Canada Ltd.'
    ENGLISH_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
    FRENCH_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
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

        product_loader = ProductItemLoader(response=response)
        # product_loader.add_value(Product.KEY_STORE, [self.store_name])
        # product_loader.add_value(Product.KEY_SOLD_BY, [self.sold_by])
        # product_loader.add_value(Product.KEY_DOMAIN, [self.domain])
        # product_loader.add_css(Product.KEY_NAME, ['div.x-product-detail-page > h1[itemprop="name"]'])
        # product_loader.add_css(Product.KEY_DESCRIPTION, ['head > meta[name="description"]::attr(content)'])
        # # product_loader.add_css(Product.KEY_RELEASE_DATE, ['#ctl00_CP_ctl00_PD_lblReleaseDate'])
        # product_loader.add_value(Product.KEY_CURRENT_OFFER, [self.__get_offer(response)])
        # product_loader.add_value(Product.KEY_URL, [response.url])
        # # product_loader.add_css(Product.KEY_AVAILABILITY, ['#schemaorg-offer > div.price-module.clearfix > div.price-wrapper.price-extra-large > link[itemprop="availability"]::attr(href)'])
        # # product_loader.add_css(Product.KEY_TAGS, ['head > meta[name="keywords"]::attr(content)'])
        # # # product_loader.add_css('brand', ['div[data-brand-bar]::attr(data-brand-bar)'])
        # # # product_loader.add_value('brand', [brand])
        return product_loader.load_item()

    def __find_json_data(self):
        pass

    def __load_with_dictionary(self, response, data):
        product_loader = ProductItemLoader(response=response)

        if not data and not data.get('product') and not data.get('product').get('product'):
            return product_loader.load_item()

        # TODO: Verify product.
        productDetails = data['product']['product']

        model_number = productDetails['modelNumber']

        try:
            upc = (UniversalProductCode(model_number)).value
        except:
            upc = None

        product_loader.add_value(Product.KEY_BRAND, productDetails['brandName'])
        product_loader.add_value(Product.KEY_MODEL_NUMBER, model_number)
        product_loader.add_value(Product.KEY_UPC, upc)
        product_loader.add_value(Product.KEY_CURRENT_OFFER, [self.__get_offer_with_dictionary(response, data)])
        product_loader.add_value(Product.KEY_STORE, [self.__get_store_with_dictionary(response, data)])
        product_loader.add_value(Product.KEY_PRODUCT_DATA, [self._get_product_data(response, data)])
        
        return product_loader.load_item()

    def _get_product_data(self, response, data):
        product_data_loader = ProductItemLoader(response=response)
        product_data_loader.add_value(ProductData.KEY_PRODUCT_DATA_RAW, [self._get_product_data_value(response, data)])
        product_data_loader.add_value(ProductData.KEY_PRODUCT_DATA_LOOKUP, [self._get_product_data_lookup(response, data)])
        return product_data_loader.load_item().get_dictionary()

    def _get_product_data_value(self, response, data):
        product_data_value_loader = ProductDataItemLoader(response=response)

        if not data and not data.get('product') and not data.get('product').get('product'):
            return product_data_value_loader.load_item()

        product = data['product']
        productDetails = product['product']
        language = data['intl']['language'] if data.get('intl') and data.get('intl').get('language') else None
        date_format_1 = self.ENGLISH_DATE_FORMAT if Language.EN == language else self.FRENCH_DATE_FORMAT
        date_format_2 = self.FRENCH_DATE_FORMAT if Language.EN == language else self.ENGLISH_DATE_FORMAT

        product_data_value_loader.add_value(ProductData.KEY_URL, response.url)
        product_data_value_loader.add_value(ProductData.KEY_NAME, [{language: productDetails['name']}])
        product_data_value_loader.add_value(ProductData.KEY_DESCRIPTION, [{language: productDetails['shortDescription']}])

        if productDetails['preorderReleaseDate']:
            try:
                date = datetime.datetime.strptime(productDetails['preorderReleaseDate'], date_format_1)
            except:
                try:
                    date = datetime.datetime.strptime(productDetails['preorderReleaseDate'], date_format_2)
                except:
                    raise

            product_data_value_loader.add_value(ProductData.KEY_RELEASE_DATE, date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat())

        model_number = productDetails['modelNumber']

        try:
            upc = (UniversalProductCode(model_number)).value
        except:
            upc = None

        product_data_value_loader.add_value(ProductData.KEY_BRAND, productDetails['brandName'])
        product_data_value_loader.add_value(ProductData.KEY_SKU, productDetails['sku'])
        product_data_value_loader.add_value(ProductData.KEY_MODEL_NUMBER, model_number)
        product_data_value_loader.add_value(Offer.KEY_SOLD_BY, [self.sold_by])
        product_data_value_loader.add_value(Offer.KEY_STORE_ID, [self.store_id])
        product_data_value_loader.add_value(ProductData.KEY_UPC, upc)

        return dict(product_data_value_loader.load_item())

    def _get_product_data_lookup(self, response, data):
        language = data['intl']['language'] if data.get('intl') and data.get('intl').get('language') else None

        product_data_lookup_loader = ProductDataLookupItemLoader(response=response)
        product_data_lookup_loader.add_value(ProductDataLookup.KEY_STORE_ID, [self.store_id])
        product_data_lookup_loader.add_value(ProductDataLookup.KEY_LANGUAGE, [language])
        product_data_lookup_loader.add_value(ProductDataLookup.KEY_UPDATED, [datetime.datetime.utcnow().isoformat()])

        return product_data_lookup_loader.load_item().get_dictionary()

    def __get_offer(self, response):
        offerLoader = OfferItemLoader(response=response)
        offerLoader.add_css(Offer.KEY_AMOUNT, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="price"]::attr(content)'])
        offerLoader.add_css(Offer.KEY_CURRENCY, ['div.x-product-detail-page span[itemprop="offers"] meta[itemprop="priceCurrency"]::attr(content)'])
        offerLoader.add_value(Offer.KEY_DATETIME, [datetime.datetime.utcnow().isoformat()])
        return dict(offerLoader.load_item())

    def __get_offer_with_dictionary(self, response, data):
        offerLoader = OfferItemLoader(response=response)

        if not data and not data.get('product') and not data.get('product').get('product'):
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
        storeLoader.add_value(Store.KEY_DOMAIN, [self.domain])
        storeLoader.add_value(Store.KEY_ID, [self.store_id])
        storeLoader.add_value(Store.KEY_NAME, [self.store_name])
        storeLoader.add_value(Store.KEY_REGION, self.region)
        return dict(storeLoader.load_item())

    def __get_availability_with_dictionary(self, product):
        productDetails = product['product']
        is_preorderable = productDetails['isPreorderable']
        shipping_purchasable = product['availability']['shipping']['purchasable']
        is_in_store_only = True if product['availability']['shipping']['status'] == Availability.IN_STORE_ONLY.value else False

        availability = Availability.UNKNOWN.value

        if is_preorderable:
            availability = Availability.PREORDER.value
        elif is_in_store_only:
            availability = Availability.IN_STORE_ONLY.value
        elif not is_preorderable and not is_in_store_only and shipping_purchasable:
            availability = Availability.IN_STOCK.value
        elif not shipping_purchasable:
            availability = Availability.OUT_OF_STOCK.value

        return availability