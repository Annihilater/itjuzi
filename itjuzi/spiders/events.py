# -*- coding: utf-8 -*-
import copy
import json
import time

import scrapy
from fake_useragent import UserAgent

from itjuzi.items import ItjuziItem
from itjuzi.settings import HEADER, AUTHORIZATIONS_URL, INVESTEVENTS_URL, PAYLOAD
from secure import ACCOUNT, PASSWORD


class EventsSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['www.itjuzi.com']
    start_urls = ['http://www.itjuzi.com/']

    def start_requests(self):
        """
        模拟POST请求登录IT桔子网
        """
        HEADER.update({"User-Agent": UserAgent().random})
        payload = {"account": ACCOUNT, "password": PASSWORD, "type": "pswd"}
        yield scrapy.Request(url=AUTHORIZATIONS_URL, method="POST", body=json.dumps(payload), headers=HEADER,
                             callback=self.parse)

    def parse(self, response):
        self.logger.debug('parse UserAgent:' + str(response.request.headers['User-Agent']))  # 输出 UA，检查是否随机
        token = json.loads(response.text)['data']['token']
        HEADER.update({"Authorization": token,
                       "User-Agent": UserAgent().random, })
        yield scrapy.Request(url=INVESTEVENTS_URL, method="POST", body=json.dumps(PAYLOAD), meta={'token': token},
                             headers=HEADER, callback=self.parse_info)

    def parse_info(self, response):
        """
        通过计算页数，获取总的页面数，抓取所有数据。
        """
        self.logger.debug('parse_info UserAgent:' + str(response.request.headers['User-Agent']))  # 输出 UA，检查是否随机
        token = response.meta["token"]  # 获取传入过来的token
        data = json.loads(response.text)
        total_number = data['data']['page']['total']  # 总数据
        if type(int(total_number) / 20) is not int:  # 总的页数
            page = int(int(total_number) / 20) + 1
        else:
            page = int(total_number) / 20
        HEADER.update({"Authorization": token,
                       "User-Agent": UserAgent().random, })
        for i in range(1, page):
            time.sleep(1)
            payload = copy.deepcopy(PAYLOAD)
            payload['page'] = i
            yield scrapy.Request(dont_filter=True, url=INVESTEVENTS_URL, method="POST", body=json.dumps(payload),
                                 headers=HEADER, callback=self.parse_detail)
            # request()中加入dont_filter=True 解决scrapy自身是默认有过滤重复请求的bug。
            # 由于parse_info()函数中 请求的url和parse_detail()函数中请求的URL相同，需要加入dont_filter=True

    def parse_detail(self, response):
        self.logger.debug('parse_detail UserAgent:' + str(response.request.headers['User-Agent']))  # 输出 UA，检查是否随机
        infos = json.loads(response.text)["data"]["data"]
        for info in infos:
            item = ItjuziItem()
            id = info["id"] if info.get('id') else '',
            com_id = info["com_id"] if info.get('com_id') else '',
            name = info["name"] if info.get('name') else '',
            com_scope = info["com_scope"] if info.get('com_scope') else '',
            money = info["money"] if info.get('money') else '',
            money_num = info["money_num"] if info.get('money_num') else '',
            valuation = info["valuation"] if info.get('valuation') else '',
            city = info["city"] if info.get('city') else '',
            agg_time = info["agg_time"] if info.get('agg_time') else '',
            invse_des = info["invse_des"] if info.get('invse_des') else '',

            for field in item.fields:
                try:
                    item[field] = eval(field)
                except NameError:
                    self.logger.debug('Field is not Defined' + field)
            yield item
