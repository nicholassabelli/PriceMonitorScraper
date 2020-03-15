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

class BestBuy(store.Store):
    store_id = 'best_buy_canada' # TODO: Constants.
    store_name = 'Best Buy'
    sold_by = 'Best Buy Canada Ltd.'
    ENGLISH_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
    FRENCH_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    region = region.Region.CANADA.value
    domain = 'bestbuy.ca'
    allowed_domains = [domain]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.strip_amount_pipeline.StripAmountPipeline': 300,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        }
    }

    def parse_product(self, response):
        data = self.__find_json_data(response)
        
        if data:
            # f = open("bbproduct.json", "w")
            # f.write(json.dumps(data))
            # f.close()
            return self.__load_with_dictionary(response, data)

        logging.warning('No product data found!')
        return None

    def __find_json_data(self, response):
        texts = response.xpath('//script/text()')

        for text in texts:
            match = text.re(".*window.__INITIAL_STATE__.*")

            if match:
                text = match[0].strip() \
                    .split('window.__INITIAL_STATE__ = ')[1]

                if text.endswith(';'):
                    text = text[:-1]
                
                try:
                    return json.loads(text)
                except:
                    pass
                
        
        return None

    def __load_with_dictionary(self, response, data):
        product_loader = product_item_loader \
            .ProductItemLoader(response=response)

        if not data and not data.get('product') \
            and not data.get('product').get('product'):
            return product_loader.load_item()

        # TODO: Verify product.
        productDetails = data['product']['product']

        model_number = productDetails['modelNumber']

        try:
            upc = (universal_product_code.UniversalProductCode(
                model_number
            )).value
        except:
            upc = None

        product_loader.add_value(
            product.Product.KEY_BRAND,
            productDetails['brandName']
        )
        product_loader.add_value(
            product.Product.KEY_MODEL_NUMBER,
            model_number
        )

        if upc:
            product_loader.add_value(
                product.Product.KEY_GTIN, 
                super()._create_gtin_field(
                    response=response, 
                    type=global_trade_item_number \
                        .GlobalTradeItemNumber.UPCA.value,
                    value=upc
                )
            )

        product_loader.add_value(
            product.Product.KEY_CURRENT_OFFER,
            self.__get_offer_with_dictionary(response, data)
        )
        product_loader.add_value(
            product.Product.KEY_STORE,
            self.__create_store_dictionary(response)
        )
        product_loader.add_value(
            product.Product.KEY_PRODUCT_DATA, 
            self.__create_product_data_dictionary(response, data, upc)
        )
        
        return product_loader.load_item()

    def __create_product_data_dictionary(self, response, data, upc):
        product_data_value_loader = \
            product_data_item_loader.ProductDataItemLoader(response=response)

        if not data and not data.get('product') \
            and not data.get('product').get('product'):
            return product_data_value_loader.load_item()

        product = data['product']
        productDetails = product['product']
        lang = data['intl']['language'] if data.get('intl') \
            and data.get('intl').get('language') else None
        date_format_1 = self.ENGLISH_DATE_FORMAT if language.Language.EN == \
            lang else self.FRENCH_DATE_FORMAT # TODO: Check best approach to comparing enums
        date_format_2 = self.FRENCH_DATE_FORMAT if language.Language.EN == \
            lang else self.ENGLISH_DATE_FORMAT

        product_data_value_loader.add_value(
            product_data.ProductData.KEY_URL,
            response.url
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_NAME,
            {lang: productDetails['name']}
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_DESCRIPTION,
            {lang: productDetails['shortDescription']}
        )

        if productDetails['preorderReleaseDate']:
            try:
                date = datetime.datetime.strptime(
                    productDetails['preorderReleaseDate'],
                    date_format_1
                )
            except:
                try:
                    date = datetime.datetime.strptime( # TODO: Test the enum evaluation.
                        productDetails['preorderReleaseDate'],
                        date_format_2
                    )
                except:
                    raise

            product_data_value_loader.add_value(
                product_data.ProductData.KEY_RELEASE_DATE,
                date.replace(
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0
                ).isoformat()
            )

        model_number = productDetails['modelNumber']

        try:
            upc = (universal_product_code.UniversalProductCode(
                model_number
            )).value
        except:
            upc = None

        product_data_value_loader.add_value(
            product_data.ProductData.KEY_BRAND,
            productDetails['brandName']
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_SKU,
            productDetails['sku']
        )
        product_data_value_loader.add_value(
            product_data.ProductData.KEY_MODEL_NUMBER,
            model_number
        )
        product_data_value_loader.add_value(
            offer.Offer.KEY_SOLD_BY,
            self.sold_by
        )
        product_data_value_loader.add_value(
            offer.Offer.KEY_STORE_ID,
            self.store_id
        )
        product_data_value_loader.add_value(
            field_name=product_data.ProductData.KEY_SUPPORTED_LANGUAGES,
            value={language.Language.EN.value: {}} # TODO: Fixed.
        )

        if upc:
            product_data_value_loader.add_value(
                product.Product.KEY_GTIN, 
                super()._create_gtin_field(
                    response=response, 
                    type=global_trade_item_number \
                        .GlobalTradeItemNumber.UPCA.value,
                    value=upc
                )
            )

        return (product_data_value_loader.load_item()).get_dictionary()

    def __determine_availability(self, product):
        productDetails = product['product']
        is_preorderable = productDetails['isPreorderable']
        shipping_purchasable = \
            product['availability']['shipping']['purchasable']
        status = product['availability']['shipping']['status']
        is_in_store_only = True if status == \
            availability.Availability.IN_STORE_ONLY.value else False
        item_availability = availability.Availability.UNKNOWN.value

        if is_preorderable:
            item_availability = availability.Availability.PREORDER.value
        elif is_in_store_only:
            item_availability = availability.Availability.IN_STORE_ONLY.value
        elif not is_preorderable and not is_in_store_only \
            and shipping_purchasable:
            item_availability = availability.Availability.IN_STOCK.value
        elif not shipping_purchasable:
            item_availability = availability.Availability.OUT_OF_STOCK.value

        return item_availability

    def __get_offer_with_dictionary(self, response, data):
        if not data and not data.get('product') and \
            not data.get('product').get('product'):
            return None

        product = data['product']
        productDetails = data['product']['product']

        return super()._create_offer_dictionary(
            response=response, 
            amount=productDetails['priceWithoutEhf'], 
            availability=self.__determine_availability(product), 
            condition=condition.Condition.NEW.value, 
            currency=curreny.Currency.CAD.value, 
            datetime=datetime.datetime.utcnow().isoformat(), 
            # sku=productDetails['sku'], 
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