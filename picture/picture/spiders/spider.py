#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from picture.items import PictureItem

class PictureSpider(Spider):
    name = "picture"
    start_urls = [
        'http://tu.duowan.com/m/meinv'
            ]

    def parse(self, response):
        selector = Selector(response)
        urls = selector.css('a ::attr(href)').extract()
        picture_urls = selector.css('img ::attr(src)').extract()
        for url in picture_urls:
            print('picture:', url)
            #yield Request(url=url, callback=self.pictureParse)
        for url in urls:
            if ('http' in url):
                print('request:', url)
                yield Request(url=url, callback=self.parse)

    def pictureParse(self, response):
        item = PictureItem()
        item['picture'] = response.body
        item['url'] = response.url
        yield item
