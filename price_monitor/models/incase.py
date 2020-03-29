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

class Incase(shopify.Shopify):
    store_id = 'incase_canada'
    store_name = "Incase Canada"
    sold_by = "Incase Designs Corp."
    region = region.Region.CANADA.value
    domain = 'incasedesigns.ca'
    allowed_domains = [
        domain,
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_monitor.pipelines.shopify_strip_amount_pipeline.ShopifyStripAmountPipeline': 300,
            # 'price_monitor.pipelines.TagsPipeline': 300,
            'price_monitor.pipelines.mongo_db_pipeline.MongoDBPipeline': 1000
        },
        'DOWNLOADER_MIDDLEWARES': {
            'price_monitor.middlewares.PriceMonitorDownloaderMiddleware': 300
        }
    }

    def _determine_language_from_url(self, url: str):
        return language.Language.EN.value

    def _find_json_data(self, response):
        return response.meta.get('js_data')