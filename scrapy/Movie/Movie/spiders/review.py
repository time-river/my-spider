#!/usr/bin/env python
# -*- coding:utf-8 -*

from scrapy.contrib.spiders import Spider 
from scrapy.selector import Selector
from scrapy.http import Request
from Movie.items import MovieReview, MovieReviewComment
import time

class ReviewSpider(Spider):
    name = "moviereview"
    start_urls = [
        'https://movie.douban.com/subject/25662329/reviews'
    ]
    
    def parse(self, response):
        selector = Selector(response)
        urls = selector.css('#content > div > div.article > div div.review').xpath('./div[contains(@class, "review-hd")]/h3/a[@title and @onclick]/@href').extract()
        print(len(urls))
        for url in urls:
            yield Request(url=url, callback=self.reviewParse)
        params = selector.css('#paginator > a.next ::attr(href)').extract()
        if params:
            raw_url = response.url.split('?')
            url = raw_url[0] + params[0]
            print(url)
            time.sleep(1)
            yield Request(url=url, callback=self.parse)
            
    def reviewParse(self, response):
        selector = Selector(response)
        review = MovieReview()
        review['id'] = selector.xpath('/html/head/meta[contains(@property, "og:url")]/@content').re(r'/(\d+)/')
        review['author'] = selector.css('#content > div > div.article > div > div.main > div.main-hd > p').xpath('./a/span[@property="v:reviewer"]/text()').extract()
        review['rating'] = selector.css('#content > div > div.article > div > div.main > div.main-hd > p').xpath('./span[@property="v:rating"]/text()').extract()
        review['time'] = selector.css('#content > div > div.article > div > div.main > div.main-hd > p').xpath('./span[@property="v:dtreviewed"]/text()').extract()
        review['title'] = selector.xpath('//*[@id="content"]/h1/span/text()').extract()
        review['content'] = selector.css('#link-report > div ::text').extract()
        vote = selector.css('#content > div > div.article > div > div.main > div.main-ft > div.main-panel > div.main-panel-useful > span > em ::text').extract()
        review['useful'] = [vote[0]]
        review['useless'] = [vote[1]]
        # comments
        review['comments'] = self.comments(selector)
        yield review
        next_page = selector.css('#comments > div.paginator > span.next > a ::attr(href)').extract()
        if next_page:
            time.sleep(10)
            yield Request(url=next_page[0], callback=self.reviewCommentsParse)
            
    def reviewCommentsParse(self, response):
        selector = Selector(response)
        comments = self.comments(selector)
        next_page = selector.css('#comments > div.paginator > span.next > a ::attr(href)').extract()
        yield comments
        if next_page:
            yield Request(url=next_page[0], callback=self.reviewCommentsParse)
            time.sleep(15)
            
    def comments(self, selector):
        comments = list()
        for item in selector.css('#comments > div.comment-item'):
            comment = MovieReviewComment()
            comment['id'] = item.css('::attr(id)').extract()
            comment['author'] = item.css('div.content > div.author > a ::text').extract()
            comment['time'] = item.css('div.content > div.author > span ::text').extract()
            comment['quote_author'] = item.css('div.content > div.reply-quote > span.pubdate > a ::text').extract()
            comment['content'] = item.css('div.content > p ::text').extract()
            comments.append(comment)
        return comments