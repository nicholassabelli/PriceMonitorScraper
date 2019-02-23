# -*- coding: utf-8 -*-

class Availability:
    IN_STOCK     = 'In Stock'
    OUT_OF_STOCK = 'Out of Stock'

class Currency:
    CAD = 'CAD'
    USD = 'USD'

class UniversalProductCode:
    LENGTH_OF_UPC = 12

    def __init__(self, upc: str):
        self.__value = ''
        self.value = upc

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, upc: str):
        # Remove leading zeros first.
        # Then turn int into a list
        upc = int(upc)
        upc_list = list(map(int, str(upc)))

        if len(upc_list) > self.LENGTH_OF_UPC or len(upc_list) < self.LENGTH_OF_UPC - 2:
            raise Exception('Blah')
        
        if self.LENGTH_OF_UPC - 2 == len(upc_list):
            upc_list.insert(0, 0)
        
        if self.LENGTH_OF_UPC - 1 == len(upc_list):
            upc_list.append(self.__calculate_check_digit(upc_list))

        self.__value = ''.join(list(map(str, upc_list)))
        
    def __calculate_check_digit(self, upc_list):
        result = 0

        for key, value in enumerate(upc_list):
            # Add the digits in the odd-numbered positions (first, third, fifth, etc.) together and multiply by three.
            # Add the digits (up to but not including the check digit) in the even-numbered positions (second, fourth, sixth, etc.) to the result.
            result += 3 * value if 0 == key % 2 or 0 == key else value
        
        # Take the remainder of the result divided by 10 (modulo operation). 
        # If the remainder is equal to 0 then use 0 as the check digit, and if not 0 subtract the remainder from 10 to derive the check digit.
        return 10 - (result % 10)

test = UniversalProductCode('000000005692001210')

print(test.value)