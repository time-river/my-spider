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
            self.logger.warning(request)
    
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
        
    async def _index_content(self, request):
        while True: # fault tolerance
            data = await self._fetch_page(request)
            if data:
               content, raw_url = data
               break
            else:
                time.sleep(30)
                # some other ways
        self.logger.debug(raw_url)
        headers = self._get_headers()
        request = {
            'url': None,
            'params': None,
            'headers': headers
        }
        return content, request
        
    async def _comments_content(self, request):
        while True: # fault tolerance
            data = await self._fetch_page(request)
            if data:
               content, raw_url = data
               break
            else:
                time.sleep(30)
                # some other ways
        self.logger.debug(raw_url)
        url = raw_url.split('?')[0]
        headers = self._get_headers()
        headers['Host'] = url.split('/')[2]
        request = {
            'url': '',
            'params': None,
            'headers': headers
        }
        return content, request
        
    def _handle_str(self, string):
        items = string.split()
        items.pop(0)
        for item in items:
            try:
                items.pop('/')
            except:
                break
            
    async def _filter_index(self, request):
        content, request = await self._index_content(request)
        selector = etree.HTML(content)
        info = {
            'name': selector.xpath('//*[@id="content"]/h1/span/text()'), # list, such as ['荒野猎人 The Revenant', '(2015)']
            'director': self._handle_str(
                selector.xpath('//*[@id="info"]/span[1]')[0].xpath('string(.)')
            ), # list
            'writer': self._handle_str(
                selector.xpath('//*[@id="info"]/span[2]')[0].xpath('string(.)')
            ),
            'actor': self._handle_str(
                selector.xpath('//*[@id="info"]/span[3]')[0].xpath('string(.)')
            ),
            'type': selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:genre")]/text()'),
        # area and language ???
            'release_date': selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:initialReleaseDate")]/text()'),
            'runtime': selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:runtime")]/text()')
        }
        if info:
            comments_url = selector.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href')[0]
            url = comments_url.split('?')[0]
            request['headers']['Host'] = url.split('/')[2]
            request['url'] = comments_url
            return info, request
        else:
            return None
    
    def _handle_rating(self, string):
        raw = re.split(r'\D', string[0])
        while True:
            try:
                raw.remove('')
            except:
                break
        try:
            return raw.pop()
        except:
            return None
            
    async def _filter_comments(self, request):
        commenters = list()
        content, request = await self._index_content(request)
        selector = etree.HTML(content)
        items = selector.xpath('//*[@class="comment"]')
        for item in items:
            commenters.append({
                'name': item.xpath('./h3/span[@class="comment-info"]/a/text()'),
                'rating': self._handle_rating(item.xpath('./h3/span[@class="comment-info"]/span[1]/@class')),
                'comment': item.xpath('./p/text()')
            })
        if commenters:
            url = selector.xpath('//*[@id="paginator"]/a[starts-with(@class, "next")]/@href')[0]
            self.logger.debug(url)
            request['url'] = '{}{}'.format(request['url'],repr(url))
            return commenters, request
        else:
            return None
            
    async def worker(self):
        request = base.blpop(self.redis, 'movie.request')
        data = await self._filter_index(request)
        if data:
            info, request = data
            info['comments'] = list()
            while True:
                data = await self._filter_comments(request)
                if data == None:
                    # deal info
                    break
                else:
                    request = data[0]
                    info['comments'].extend(data[1])
                           
    def run(self):
        self.logger.info('----------start----------')
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.worker())
        loop.close()
        self.logger.info('----------^end^----------')
    
if __name__ == '__main__':
    spider = Download()
    spider.run()