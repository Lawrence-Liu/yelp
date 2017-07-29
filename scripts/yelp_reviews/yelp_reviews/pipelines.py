# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter


class YelpReviewsPipeline(object):
    def process_item(self, item, spider):
        item['review_score'] = float(item['review_score'][0:3])
        item['review_text'] = re.sub('<[^>]*>', '', item['review_text'])
        item['review_date'] = re.sub('\s', '', item['review_date'])
        return item

class WriteCsvPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('~/PycharmProjects/yelp/data/reviews.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item