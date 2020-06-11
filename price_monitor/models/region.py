# -*- coding: utf-8 -*-

from enum import Enum

"""Defines regions in ISO 3166-1 alpha-2 format.

    https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#AS
"""
class Region(Enum):
    CANADA = 'CA'
    UNITED_STATES_OF_AMERICA = 'US'