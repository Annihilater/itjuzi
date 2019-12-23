#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/12/23 9:37 上午
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : events_spider.py


from scrapy import cmdline

cmdline.execute('scrapy crawl events'.split())
