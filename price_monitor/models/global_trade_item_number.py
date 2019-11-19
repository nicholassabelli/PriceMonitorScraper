# -*- coding: utf-8 -*-

from enum import Enum

class GlobalTradeItemNumber(Enum):
    UPCA = 'UPC-A'
    UPCE = 'UPC-E'
    EAN13 = 'EAN-13'
    EAN8 = 'EAN-8'
    ISBN10 = 'ISBN-10'
    ISBN13 = 'ISBN-13'
    ISSN = 'ISSN'
