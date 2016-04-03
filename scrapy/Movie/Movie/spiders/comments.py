#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import Spider 
from scrapy.selector import Selector
from scrapy.http import Request
from Movie.items import MovieComment

class CommentSpider(Spider):
    name = "moviecomment"
    start_urls = [
        
    ]
    
    def parse(self, response):
        comments = list()
        selector = Selector(response)
        items = selector.css('#comments  div.comment-item > div.comment') # div并不一定是#comments的孩子
        for item in items:
            comment = MovieComment()
            comment['id'] = item.css('h3 > span.comment-info > a ::attr(href)').re(r'[\d]+')
            comment['author'] = item.css('h3 > span.comment-info > a ::text').extract()
            comment['rating'] = item.css('h3 > span.comment-info > span.rating ::attr(class)').re(r'[1-5]') 
            comment['time'] = item.css('h3 > span.comment-info > span ::text').extract()
            comment['content'] = item.css('p ::text').extract()
            comment['vote'] = item.css('h3 > span.comment-vote > span ::text').extract()
            comments.append(comment)
    #    yield comments
        params = selector.css('#paginator > a ::attr(href)').extract()
        if params:
            raw_url = response.url.split('?')
            url = raw_url[0] + params[0]
            yield Request(url=url, callback=parse)

