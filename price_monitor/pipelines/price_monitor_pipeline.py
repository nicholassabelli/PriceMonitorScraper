# -*- coding: utf-8 -*-

class PriceMonitorPipeline(object):
    def process_item(self, item, spider):
        return item