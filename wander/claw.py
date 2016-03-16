#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
抓取网页类 - 协程 -
参数
concurrency  协程数量
redis        redis实例
request_key  redis中存储的HTTP请求key 反序列化后的数据格式 {'url': 请求url, 'params': 查询参数, 'headers': 请求头, 'type': 抓取的数据类型}
content_key  redis中存储的抓取内容key  反序列化后的数据格式 str或json
proxy_key    redis中存储的的代理key    反序列化后的数据格式 {'ip': ip地址, 'port': 端口, 'protocol': 协议}
方法
_fetch_page(session, request) 根据request存储的信息获取html，并把content序列化后存入redis。若request超时，则重新获取session
_get_session()                若proxy_key不为None，则返回值为使用代理的session
_worker()                     获取session & request，调用_fet_page()。直至无可用的session - 使用proxy时候 - 或者 无可用的request为止               
'''

import logging
import asyncio
from asyncio import Queue
import aiohttp
import pickle
from base import redis_push, redis_pop

class Claw:
    def __init__(self, concurrency=5, *, redis, request_key, content_key, proxy_key=None):
        self.concurrency = concurrency
        # redis
        self.redis = redis
        self.proxy_key = proxy_key
        self.request_key = request_key
        self.content_key = content_key
        
    async def _fetch_page(self, session, request):
        try:
            with aiohttp.Timeout(10):
                async with session.get(request['url'], params=request['params'], headers=request['headers']) as response:
                    try:
                        assert response.status == 200
                        if request['type'] is 'json':
                            content = await response.json()
                        else:
                            content = await response.text(request['type'])
                        redis_push(self.redis, self.content_key, content)
                    except AssertionError:
                        logging.warning('{} {}'.format(response.status, url))
        except: # kinds of error, not only asyncio.TimeoutError
            session.close() # close session
            logging.error('Timeout  {}'.format(request['url']), 'and will try again latter')
            redis_push(self.redis, self.request_key, request)
            session = self._get_session()
        finally:
            return session
            
    def _get_session(self):
        if self.proxy_key:
            proxy = redis_pop(self.redis, self.proxy_key)
            if proxy:
                addr = proxy['protocol'] + '://' + proxy['ip'] +':'+proxy['port']
                conn = aiohttp.ProxyConnector(proxy=addr)
                session = aiohttp.ClientSession(connector=conn)
                return session
            else:
                return None
        else:
            return aiohttp.ClientSession()
                       
    async def _worker(self):
        session = self._get_session()
        while True:
            if session:
                request = redis_pop(self.redis, self.request_key)
                if request:
                    print('claw {} {}'.format(request['url'], request['params']))
                    session = await self._fetch_page(session, request)
                else:
                    session.close()
                    break
            else:
                break
            
    def main(self):
        print('##########claw start##########')
        loop = asyncio.get_event_loop()
        fs = asyncio.wait([self._worker() for _ in range(self.concurrency)])
        loop.run_until_complete(fs)
        loop.close()
        print('##########claw end##########')