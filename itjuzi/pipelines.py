# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import copy

import pymongo

from itjuzi.items import ItjuziItem


class ItjuziPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        """
        在爬虫启动的时候执行 open_spider 方法
        创建 mongodb 连接客户端
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        pass

    def process_item(self, item, spider):
        name = item.__class__.__name__
        if isinstance(item, ItjuziItem):
            if not self.db[name].find_one({'name': item['name'], 'com_id': item['com_id']}):
                self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        """
        爬虫结束的时候执行 close_spider 方法
        关闭 mongodb 连接客户端
        """
        self.client.close()
