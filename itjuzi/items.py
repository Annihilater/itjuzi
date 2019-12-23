# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    com_id = scrapy.Field()
    name = scrapy.Field()
    com_scope = scrapy.Field()
    money = scrapy.Field()
    money_num = scrapy.Field()
    valuation = scrapy.Field()
    city = scrapy.Field()
    agg_time = scrapy.Field()
    invse_des = scrapy.Field()
