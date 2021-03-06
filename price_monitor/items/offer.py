from scrapy import (
    Field,
    Item,
)
from scrapy.utils.project import get_project_settings

class Offer(Item):
    # Array indexes.
    KEY_AMOUNT = 'amount'
    KEY_AVAILABILITY = 'availability'
    KEY_CONDITION = 'condition'
    KEY_CREATED = 'created'
    KEY_CURRENCY = 'currency'
    KEY_DATETIME = 'datetime' 
    KEY_END_DATE = 'end_date' # TODO: End date, some stores provide this info.
    KEY_ID = '_id'  
    KEY_PRODUCT_ID = 'product_id'
    # KEY_SKU = 'sku' # TODO: SKU is bad for offer, store could reuse for all items in a case.
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    KEY_UPDATED = 'updated'
    KEY_VERSION = 'version' # Not an item field.

    # Fields.
    amount = Field()
    availability = Field()
    condition = Field()
    created = Field()
    currency = Field()
    datetime = Field()
    end_date = Field()
    product_id = Field()
    # sku = Field()
    sold_by = Field()
    store_id = Field()
    updated = Field()



    # warranty
    # is_on_sale = Field()
    # region
    # saleEndDate
    # isPreorder
    # shipping
    # customerRating
    # customerRatingCount
    # seller
    # is_third_party_seller
    # is_online_only
    # specialOffers
    # warranties
    

    # KEY_REGION = 'region'
    # region = Field()

    def get_dictionary(self):
        dictionary = dict(self)
        dictionary[self.KEY_VERSION] = self.get_version()
        return dictionary

    def get_version(self):
        return get_project_settings().get('OFFER_ITEM_VERSION')