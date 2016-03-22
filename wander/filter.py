#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing
from base import redis_pop, redis_push
    
class Filter:
    def __init__(self, filter, rules=None, *, redis, content_key=None, raw_proxy_key=None):
        self.filter = filter
        self.rules = rules
        # redis
        self.redis = redis
        self.content_key = content_key
        self.raw_proxy_key = raw_proxy_key
                
    def _run(self):
        while True:
            obj = redis_pop(self.redis, self.content_key)
            if not obj:
                break
            data = self.filter(obj['content'], self.rules[obj['order']])
            if data:
                redis_push(self.redis, self.raw_proxy_key, data)
        
    def main(self):
        num = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(num)
        for _ in range(num):
            pool.apply_async(self._run)
        pool.close()
        pool.join()
        self._run()
