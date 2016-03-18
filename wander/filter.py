#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import multiprocessing
from base import redis_pop, redis_push

class Filter:
    def __init__(self, filter, *, redis, content_key=None, raw_proxy_key=None):
        self.filter = filter
        # redis
        self.redis = redis
        self.content_key = content_key
        self.raw_proxy_key = raw_proxy_key
        
    def _run(self):
        while True:
            content = redis_pop(self.redis, self.content_key)
            if not content:
                print('filter break')
                break
            data = self.filter(content)
            if data:
                redis_push(self.redis, self.raw_proxy_key, data)
        
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
