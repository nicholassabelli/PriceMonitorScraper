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

class Leons(store.Store): # Is shopify.
    store_id = 'leons_canada' # TODO: Constants.
    store_name = "Leon's"
    sold_by = "Leon's Furniture Ltd."
    region = region.Region.CANADA.value
    domain = 'leons.ca'
    allowed_domains = [domain] # TODO: French domain is different.
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.the_brick_strip_amount_pipeline.TheBrickStripAmountPipeline': 300,
            # 'price_monitor.pipelines.TagsPipeline': 300,
            # 'price_monitor.pipelines.MongoDBPipeline': 1000
        }
    }

    def parse_product(self, response):
        data = self.__find_json_data(response)
        
        if data:
            return self.__load_with_dictionary(response, data)

        logging.warning('No product data found!')
        return None

    def _get_availability_with_dictionary(self, data):
        return availability.Availability.IN_STOCK.value if data \
            else availability.Availability.OUT_OF_STOCK.value

    def __find_json_data(self, response):
        text = response.css('script[data-product-json]::text').get()   

        if text:
            return json.loads(text)
        
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
                super()._get_gtin_field(
                    response=response, 
                    type=global_trade_item_number
                        .GlobalTradeItemNumber.UPCA.value, 
                    value=upc
                )
            )

        product_loader.add_value(product.Product.KEY_BRAND, data['vendor'])
        product_loader.add_value(
            product.Product.KEY_CURRENT_OFFER, 
            self.__get_offer_with_dictionary(response, data)
        )
        product_loader.add_value(
            product.Product.KEY_STORE, 
            self.__get_store_with_dictionary(response)
        )
        product_loader.add_value(
            product.Product.KEY_PRODUCT_DATA, 
            self.__get_product_data(response, data, upc)
        )
        
        return product_loader.load_item()

    def __get_product_data(self, response, data, upc):
        product_data_value_loader = \
            product_data_item_loader.ProductDataItemLoader(response=response)

        lang = language.Language.EN.value

        if upc:
            product_data_value_loader.add_value(
                product.Product.KEY_GTIN, 
                super()._get_gtin_field(
                    response=response, 
                    type=global_trade_item_number \
                        .GlobalTradeItemNumber.UPCA.value, 
                    value=upc
                )
            )

        product_data_value_loader.add_value(
            product_data.ProductData.KEY_URL, 
            response.url
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_NAME, 
            super()._get_text_field(
                response=response, 
                value=data['title'].split('|')[0], 
                language=language.Language.EN.value)
            )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_DESCRIPTION, 
            super()._get_text_field(
                response=response, 
                value=data['description'], 
                language=language.Language.EN.value)
            )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_BRAND, 
            data['vendor']
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_SKU, 
            data['variants'][0]['sku']
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_MODEL_NUMBER, 
            data['tags']['vsn']
        )
        product_data_value_loader.add_value(
            offer.Offer.KEY_SOLD_BY,
            self.sold_by
        )
        product_data_value_loader.add_value(
            offer.Offer.KEY_STORE_ID, 
            [self.store_id]
        )

        return (product_data_value_loader.load_item()).get_dictionary()

    def __get_offer_with_dictionary(self, response, data):
        return super()._get_offer_with_dictionary(
            response=response, 
            amount=data['price'], 
            availability=data['available'], 
            condition=condition.Condition.NEW.value, 
            currency=curreny.Currency.CAD.value, 
            datetime=datetime.datetime.utcnow().isoformat(), 
            sku=data['tags']['vsn'], 
            sold_by=self.sold_by, 
            store_id=self.store_id
        )

    def __get_store_with_dictionary(self, response):
        return super()._get_store_with_dictionary(
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