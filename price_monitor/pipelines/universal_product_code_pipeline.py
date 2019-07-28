# -*- coding: utf-8 -*-

from price_monitor.pipelines.price_monitor_pipeline import PriceMonitorPipeline

class UniversalProductCodePipeline(PriceMonitorPipeline):
    def process_item(self, item, spider):
        return item