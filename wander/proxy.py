#!/usr/bin/env python
# -*- coding:utf-8 -*-

import asyncio
import aiohttp
import random
from base import redis_push, redis_pop, redis_sadd, redis_smembers, redis_srem
    
class Proxy:
    def __init__(self, use_https_proxy=False, *, redis, raw_proxy_key=None, proxy_key=None):
        self.use_https_proxy = use_https_proxy # don't use now
        self.concurrency = 50
        # redis
        self.redis = redis
        self.raw_proxy_key = raw_proxy_key
        self.proxy_key = proxy_key
        self.test_url = [
            #'https://www.hao123.com/',
            #'https://www.baidu.com/',
            'http://tieba.baidu.com/',
            'http://news.baidu.com/',
            'http://zhidao.baidu.com/',
            'http://music.baidu.com/',
            'http://image.baidu.com/',
            'http://v.baidu.com/',
            'http://map.baidu.com/',
            'http://baike.baidu.com/',
            'http://wenku.baidu.com/',
            #'https://www.jd.com/',
            #'https://www.douban.com/',
            #'https://movie.douban.com/',
            #'https://book.douban.com/',
            #'https://music.douban.com/',
            'http://dongxi.douban.com/',
            #'https://www.alipay.com/',
            #'https://www.taobao.com/',
            #'https://www.1688.com/',
            #'https://www.tmall.com/',
            'http://www.sina.com.cn/',
            'http://www.weibo.com/',
            'http://www.163.com/',
            'http://www.qq.com/',
            'http://i.qq.com/',
            'http://www.weiyun.com/',
            'http://www.youku.com/',
            'http://www.sohu.com/',
            'http://www.ganji.com/',
            'http://xa.58.com/'
        ]
        
    async def _verify_proxy(self, proxy):
        addr = proxy['protocol'] + '://' + proxy['ip'] +':'+proxy['port']
        conn = aiohttp.ProxyConnector(proxy=addr)
        try:
            session = aiohttp.ClientSession(connector=conn)
            with aiohttp.Timeout(10):
                async with session.get(self.test_url[random.randrange(len(self.test_url))]) as response: # close connection and response, otherwise will tip: Unclosed connection and Unclosed response
                    try:
                        assert response.status == 200
                        redis_sadd(self.redis, self.proxy_key, proxy)
                    except: 
                        pass      
        except: #ProxyConnectionError, HttpProxyError and etc?
            pass
        finally:
            session.close() # close session when timeout
            
    async def _worker(self):
        while True:
            proxy = redis_pop(self.redis, self.raw_proxy_key)
            if proxy:
                if proxy['protocol'] == 'https':
                     continue
                await self._verify_proxy(proxy)
            else:
                break
                
    async def _monitor_worker(self):
        key = 'monitor.proxy'
        data = redis_smembers(self.redis, self.proxy_key)
        redis_push(self.redis, key, data)
        while True:
            proxy = redis_pop(self.redis, key)
            redis_srem(self.redis, self.proxy_key, proxy) # 有罪待定
            if proxy:
                if proxy['protocol'] == 'https':
                    continue
                await self._verify_proxy(proxy)
                await asyncio.sleep(1)
            else:
                break
            
    def main(self):
        loop = asyncio.get_event_loop()
        fs = asyncio.wait([self._worker() for _ in range(self.concurrency)])
        loop.run_until_complete(fs)
        loop.close()
        
    def monitor(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._monitor_worker())
        loop.close()