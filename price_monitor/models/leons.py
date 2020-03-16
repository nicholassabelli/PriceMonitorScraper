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
    shopify,
    universal_product_code
)

class Leons(shopify.Shopify):
    store_id = 'leons_canada'
    store_name = "Leon's"
    sold_by = "Leon's Furniture Ltd."
    region = region.Region.CANADA.value
    domain = 'leons.ca'
    allowed_domains = [
        domain,
    ]

    def _determine_language_from_url(self, url: str):
        if re.search(f'www.{self.domain}', url):
            return language.Language.EN.value
        elif re.search(f'fr.{self.domain}', url):
            return language.Language.FR.value
        
        return None

    def _create_product_data_dictionary(self, response, data, upc):
        super()._create_product_data_dictionary(response, data, upc)

        # The description holds extra data separated by ";;;;".
        descData = data['description'].split(';;;;')
        name = None
        desc = None

        if self.language == language.Language.EN.value:
            name = data['title'].split('|')[0]
            desc = descData[0]
        elif self.language == language.Language.FR.value:
            name = descData[1]
            desc = descData[2]
        else:
            pass # TODO: Error.

        self.product_data_value_loader.replace_value(
            field_name=product_data.ProductData.KEY_NAME, 
            value=super()._create_text_field(
                response=response, 
                value=name, 
                language=self.language
            )
        )
        self.product_data_value_loader.replace_value(
            field_name=product_data.ProductData.KEY_DESCRIPTION, 
            value=super()._create_text_field(
                response=response, 
                value=desc, 
                language=self.language
            )
        )

        return (self.product_data_value_loader.load_item()).get_dictionary()