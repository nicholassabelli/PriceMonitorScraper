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

class TheBrick(shopify.Shopify): # Is shopify.
    store_id = 'the_brick_canada' # TODO: Constants.
    store_name = 'The Brick'
    sold_by = 'The Brick Ltd.'
    region = region.Region.CANADA.value
    domain = 'thebrick.com'
    domain_fr = 'brickenligne.com'
    allowed_domains = [
        domain,
        domain_fr
    ]

    def _determine_language_from_url(self, url: str):
        if re.search(self.domain, url):
            return language.Language.EN.value
        elif re.search(self.domain_fr, url):
            return language.Language.FR.value
        
        return None