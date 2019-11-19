# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Offer(Item): # TODO: Rename to offer.
    # Array indexes.
    KEY_AMOUNT = 'amount'
    KEY_AVAILABILITY = 'availability'
    KEY_CONDITION = 'condition'
    KEY_CREATED = 'created'
    KEY_CURRENCY = 'currency'
    KEY_DATETIME = 'datetime'  
    KEY_ID = '_id'  
    KEY_PRODUCT_ID = 'product_id'
    KEY_SKU = 'sku' # TODO: SKU is bad for offer, store could reuse for all items in a case.
    KEY_SOLD_BY = 'sold_by'
    KEY_STORE_ID = 'store_id'
    KEY_UPDATED = 'updated'
    
    # Fields.
    amount = Field()
    availability = Field()
    condition = Field()
    created = Field()
    currency = Field()
    datetime = Field()
    product_id = Field()
    sku = Field()
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