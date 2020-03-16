import datetime
import logging
import json
import re
from price_monitor.items import (
    offer,
    product,
    product_data
)
from price_monitor.item_loaders import (
    product_item_loader,
    product_data_item_loader
)
from price_monitor.models import (
    availability,
    condition,
    curreny,
    global_trade_item_number,
    language,
    region,
    store,
    universal_product_code
)

class Shopify(store.Store): 
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.shopify_strip_amount_pipeline.ShopifyStripAmountPipeline': 300,
            # 'price_monitor.pipelines.TagsPipeline': 300,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        }
    }

    def parse_product(self, response):
        self.language = self._determine_language_from_url(response.url)

        if not self.language:
            logging.error('Unable to determine language!')
            return None

        data = self.__find_json_data(response)
        
        if data:
            return self.__load_with_dictionary(response, data)

        logging.warning('No product data found!')
        return None

    def _determine_availability(self, data):
        return availability.Availability.IN_STOCK.value if data \
            else availability.Availability.OUT_OF_STOCK.value

    def __find_json_data(self, response):
        text = response.css('script[data-product-json]::text').get()   

        if text:
            try:
                return json.loads(text)
            except:
                logging.error('Unable to load JSON data.')
                pass
        
        return None

    def __load_with_dictionary(self, response, data):
        product_loader = product_item_loader.ProductItemLoader(
            response=response
        )

        data['tags'] = self.__parse_tags(data['tags'])

        try:
            upc = (universal_product_code.UniversalProductCode(
                data['tags']['upc'])
            ).value
        except:
            upc = None

        if upc:
            product_loader.add_value(
                product.Product.KEY_GTIN, 
                super()._create_gtin_field(
                    response=response, 
                    type=global_trade_item_number
                        .GlobalTradeItemNumber.UPCA.value, 
                    value=upc
                )
            )

        product_loader.add_value(product.Product.KEY_BRAND, data['vendor'])
        product_loader.add_value(
            product.Product.KEY_CURRENT_OFFER, 
            self.__create_offer_dictionary(response, data)
        )
        product_loader.add_value(
            product.Product.KEY_MODEL_NUMBER, 
            data['tags']['vsn']
        )
        product_loader.add_value(
            product.Product.KEY_PRODUCT_DATA, 
            self._create_product_data_dictionary(response, data, upc)
        )
        product_loader.add_value(
            product.Product.KEY_STORE, 
            self.__create_store_dictionary(response)
        )
        
        return product_loader.load_item()

    def _create_product_data_dictionary(self, response, data, upc):
        self.product_data_value_loader = \
            product_data_item_loader.ProductDataItemLoader(response=response)

        if upc:
            self.product_data_value_loader.add_value(
                field_name=product.Product.KEY_GTIN, 
                value=super()._create_gtin_field(
                    response=response, 
                    type=global_trade_item_number \
                        .GlobalTradeItemNumber.UPCA.value, 
                    value=upc
                )
            )

        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_URL, 
            value=response.url
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_NAME, 
            value=super()._create_text_field(
                response=response, 
                value=data['title'].split('|')[0], 
                language=self.language
            )
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_DESCRIPTION, 
            value=super()._create_text_field(
                response=response, 
                value=data['description'], 
                language=self.language
            )
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_BRAND, 
            value=data['vendor']
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_SKU, 
            value=data['variants'][0]['sku']
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_MODEL_NUMBER, 
            value=data['tags']['vsn']
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_SOLD_BY,
            value=self.sold_by
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_STORE_ID, 
            value=self.store_id
        )
        self.product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
            value={self.language: {}} # TODO: Fix.
        )

        return (self.product_data_value_loader.load_item()).get_dictionary()

    def __create_offer_dictionary(self, response, data):
        return super()._create_offer_dictionary(
            response=response, 
            amount=data['price'], 
            availability=data['available'], 
            condition=condition.Condition.NEW.value, 
            currency=curreny.Currency.CAD.value, 
            sold_by=self.sold_by, 
            store_id=self.store_id
        )

    def __create_store_dictionary(self, response):
        return super()._create_store_dictionary(
            response=response, 
            domain=self.domain, 
            store_id=self.store_id, 
            store_name=self.store_name, 
            region=self.region
        )

    def __parse_tags(self, tags):
        result = dict()

        for entry in tags:
            if re.search(':', entry):
                split = entry.split(':')
                result[split[0]] = split[1]
        
        return result