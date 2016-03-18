#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import asyncio
from asyncio import Queue
import aiohttp
import pickle
from base import redis_push, redis_pop

class Claw:
    def __init__(self, concurrency=5, *, redis, request_key, content_key):
        self.concurrency = concurrency
        # redis
        self.redis = redis
        self.request_key = request_key
        self.content_key = content_key
        
    async def _fetch_page(self, request):
        try:
            with aiohttp.Timeout(10):
                async with aiohttp.get(request['url'], params=request['params'], headers=request['headers']) as response:
                    try:
                        assert response.status == 200
                        if request['type'] == 'json':
                            content = await response.json()
                        else:
                            content = await response.text(request['type'])
                        redis_push(self.redis, self.content_key, content)
                    except AssertionError:
                        logging.warning('{} {}'.format(response.status, url))
        except: # kinds of error, not only asyncio.TimeoutError
            logging.error('Timeout  {}'.format(request['url']), 'and will try again latter')
            redis_push(self.redis, self.request_key, request)
                       
    async def _worker(self):
        while True:
            request = redis_pop(self.redis, self.request_key)
            if request:
                print('claw {} {}'.format(request['url'], request['params']))
                await self._fetch_page(session, request)
            else:
                break
                            
    def main(self):
        print('##########claw start##########')
        loop = asyncio.get_event_loop()
        fs = asyncio.wait([self._worker() for _ in range(self.concurrency)])
        loop.run_until_complete(fs)
        loop.close()
        print('##########claw end##########')
