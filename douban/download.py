#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import logging
import asyncio
from asyncio import Queue
import aiohttp
from lxml import etree
import redis
import base
import time
import re


    
class Download:
    def __init__(self):
        info = base.redis_login()
        self.redis = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
        self.logger = base.get_log(name="download")
        
        
    async def _fetch_page(self, request):
        try:
            with aiohttp.Timeout(10):
                async with aiohttp.get(request['url'], params=request['params'], headers=request['headers']) as response:
                    try:
                        assert response.status == 200
                        return await response.text(), response.url
                    except AssertionError:
                        self.logger.warning('{} {}'.format(response.status, url))
        except:
            self.logger.warning('{} failed'.format(request['params']))
    
    def _get_headers(self):
        headers = {
            'User-Agent': base.srandmember(self.redis, 'user.agent'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': base.srandmember(self.redis, 'referer')
        }
        return headers
        
    async def _get_content(self, request):
        while True: # fault tolerance
            data = await self._fetch_page(request)
            if data:
               content, raw_url = data
               break
            else:
                time.sleep(30)
                # some other ways
        self.logger.debug(raw_url)
        url, sign, num = re.split(r'\?|=', raw_url)
        headers = self._get_headers()
        headers['Host'] = url.split('/')[2]
        request = {
            'url': url,
            'params': {
                sign: repr(int(num)+15)
            },
            'headers': headers
        }
        return content, request
        
    def _next_request(self, urls):
        request_list = list()
        for raw_url in urls:
            url = raw_url.split('?')[0]
            headers = self._get_headers()
            headers['Host'] = url.split('/')[2]
            request = {
                'url': url,
                'params': None,
                'headers': headers
            }
            request_list.append(request)
        base.rpush(self.redis, 'movie.request', request_list)
            
    async def _filter_page(self, request):
        content, request = await self._get_content(request)
        selector = etree.HTML(content)
        urls = selector.xpath('//dd/a/@href')
        if urls:
            self.logger.debug('urls number: {}\n{}'.format(len(urls), urls))
            self._next_request(urls)
            return request
        else:
            return None
        
    async def worker(self):
        request = base.blpop(self.redis, 'douban.movie.request')
        while True:
            request = await self._filter_page(request)
            if request == None:
                break
                           
    def run(self):
        self.logger.info('----------start----------')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.worker())
        loop.close()
        self.logger.info('----------^end^----------')
    
if __name__ == '__main__':
    spider = Download()
    spider.run()