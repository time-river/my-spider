#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
过滤类 - 多进程 -
参数
filter       过滤规则方法。返回值是一个tuple - (data, request) - 若request是str类型，则代表data存入redis，request为key，比如proxy；若request非str类型，则代表request为待使用的request，data存入MongoDB
redis        redis实例
request_key  redis中存储的HTTP请求key 反序列化后的数据格式 {'url': 请求url, 'params': 查询参数, 'headers': 请求头, 'type': 抓取的数据类型}
content_key  redis中存储的抓取内容key  反序列化后的数据格式 str或json
方法
_run()       从redis中获取并处理content，直至不存在content
'''

import logging
import multiprocessing
import pymongo
from base import redis_pop, redis_push # mongo_input

class Filter:
    def __init__(self, filter, *, redis, content_key, request_key=None):
        self.filter = filter
        # redis
        self.redis = redis
        self.content_key = content_key
        self.request_key = request_key
        #self.mongo = 
        
    def _run(self):
        while True:
            content = redis_pop(self.redis, self.content_key)
            if not content:
                print('filter break')
                break
            data, request = self.filter(content)
            if data:
                if isinstance(request, str):
                    redis_push(self.redis, request, data)
                else:
                    pass
                    # redis transactions
                    redis_push(self.redis, self.request_key, request)
        
    def main(self):
        print('----------filter start----------')
        num = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num)
        for _ in range(num):
            pool.apply_async(self._run)
        pool.close()
        pool.join()
        self._run()
        print('----------filter end----------')
