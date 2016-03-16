#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
验证代理类 - 协程 -
参数
test_url        测试url
use_https_proxy 是否使用https代理 -- 功能暂时未添加
redis           redis实例
raw_proxy_key   redis中存储的未验证的代理key  反序列化后的格式同proxy_key
proxy_key       redis中存储的的代理key       反序列化后的数据格式 {'ip': ip地址, 'port': 端口, 'protocol': 协议}
方法
_verify_proxy(proxy)   验证proxy，若可用则存入redis中
_verify_worker()       从redis中获取为验证的proxy，并调用_verify_proxy，直至无可用raw_proxy
'''

import logging
import asyncio
import aiohttp
from base import redis_push, redis_pop

class Proxy:
    def __init__(self, test_url, use_https_proxy=False, *, redis, raw_proxy_key, proxy_key):
        self.test_url = test_url
        self.use_https_proxy = use_https_proxy # don't use now
        self.concurrency = 15
        # redis
        self.redis = redis
        self.raw_proxy_key = raw_proxy_key
        self.proxy_key = proxy_key
        
    async def _verify_proxy(self, proxy):
        addr = proxy['protocol'] + '://' + proxy['ip'] +':'+proxy['port']
        conn = aiohttp.ProxyConnector(proxy=addr)
        try:
            session = aiohttp.ClientSession(connector=conn)
            with aiohttp.Timeout(10):
                async with session.get(self.test_url) as response: # close connection and response, otherwise will tip: Unclosed connection and Unclosed response
                    try:
                        assert response.status == 200
                        print('Good proxy: {}'.format(proxy['ip']))
                        redis_push(self.redis, self.proxy_key, proxy)
                    except: 
                        print('Bad proxy: {}, {}'.format(proxy['ip'], response.status))        
        except: #ProxyConnectionError, HttpProxyError and etc?
            print("{} timeout".format(proxy['ip']))
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
            
    def main(self):
        print('~~~~~~~~~~proxy verification start~~~~~~~~~~')
        loop = asyncio.get_event_loop()
        fs = asyncio.wait([self._worker() for _ in range(self.concurrency)])
        loop.run_until_complete(fs)
        loop.close()
        print('~~~~~~~~~~proxy verification end~~~~~~~~~~')