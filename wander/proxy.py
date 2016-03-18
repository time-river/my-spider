#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import asyncio
import aiohttp
from base import redis_push, redis_pop

class Proxy:
    def __init__(self, test_url, use_https_proxy=False, *, redis, raw_proxy_key=None, proxy_key=None):
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
                        bfs.add(proxy)
                    except: 
                        print('Bad proxy: {}, {}'.format(proxy['ip'], response.status))        
        except: #ProxyConnectionError, HttpProxyError and etc?
            print("{} timeout".format(proxy['ip']))
        finally:
            session.close() # close session when timeout
            
    async def _worker(self):
        while True:
            proxy = redis_pop(self.redis, self.raw_proxy_key)
            if proxy and (not(proxy in bfs)): # boom filter
                if proxy['protocol'] == 'https':
                    continue
                await self._verify_proxy(proxy)
            else:
                break
                
    async def _loop_worker(self):
        while True:
            proxy = redis_pop(self.redis, self.raw_proxy_key)
            if proxy:
                if proxy['protocol'] == 'https':
                    continue
                await self._verify_proxy(proxy)
                await asyncio.sleep(1)
            else:
                break
            
    def main(self):
        print('~~~~~~~~~~proxy verification start~~~~~~~~~~')
        loop = asyncio.get_event_loop()
        fs = asyncio.wait([self._worker() for _ in range(self.concurrency)])
        loop.run_until_complete(fs)
        loop.close()
        print('~~~~~~~~~~proxy verification end~~~~~~~~~~')
        
    def loop_main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(_loop_worker())
        loop.close()