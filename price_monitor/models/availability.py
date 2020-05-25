# -*- coding: utf-8 -*-

from enum import Enum

class Availability(Enum):
    DISCONTINUED = 'Discontinued'
    IN_STOCK = 'InStock'
    IN_STORE_ONLY = 'InStoreOnly'
    LIMITED_AVAILABILITY = 'LimitedAvailability'
    ONLINE_ONLY = 'OnlineOnly'
    OUT_OF_STOCK = 'OutOfStock'
    PREORDER = 'PreOrder'
    PRESALE = 'PreSale'
    SOLD_OUT = 'SoldOut'
    UNKNOWN = 'Unknown'