# -*- coding: utf-8 -*-

from scrapy import Item, Field

class Offer(Item): # TODO: Rename to offer.
    # Array indexes.
    KEY_AMOUNT = 'amount'
    
    KEY_CURRENCY = 'currency'
    KEY_DATETIME = 'datetime'


    # New.
    KEY_AVAILABILITY = 'availability'

    # Fields.
    amount = Field()
    
    currency = Field()
    datetime = Field()

    # New.
    availability = Field()
    condition = Field()
    isOnSale = Field()

    #ehf
    #saving
    #saleEndDate
    #isPreorder
    #shipping
    #customerRating
    #customerRatingCount
    #seller
    #


