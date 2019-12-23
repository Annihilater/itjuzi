# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import copy

import pymongo


class ItjuziPipeline(object):
    def process_item(self, item, spider):
        return item


# mongodb pipeline
class ItjuziMongoPipeline():
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
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        问题：数据存入数据库之后，出现大量重复数据
        解决思路：
        在process_item中执行数据插入之前，先对变量进行复制copy，再用复制copy的变量进行操作，通过互斥确保变量不被修改。因此，修正这个问题，我们只需要调整优化下process_item()方法。
        解决代码：process_item()     - copy.deepcopy(item)   ->导入copy包
        """
        asynItem = copy.deepcopy(item)
        infos = {'id': asynItem['id'],
                 'com_id': asynItem['com_id'],
                 'name': asynItem['name'],
                 'com_scope': asynItem['com_scope'],
                 'money': asynItem['money'],
                 'money_num': asynItem['money_num'],
                 'valuation': asynItem['valuation'],
                 'city': asynItem['city'],
                 'agg_time': asynItem['agg_time'],
                 'invse_des': asynItem['invse_des'],
                 }
        self.db.ITjuzi.insert(infos)
        return item
