# -*- coding: utf-8 -*-

from enum import Enum

class Condition(Enum):
    DAMAGED = 'Damaged'
    NEW = 'New'
    REFURBISHED = 'Refurbished'
    USED = 'Used'
    UNKNOWN = 'Unknown'

# DamagedCondition
# NewCondition
# RefurbishedCondition
# UsedCondition