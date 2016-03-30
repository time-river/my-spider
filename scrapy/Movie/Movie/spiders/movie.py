#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import Spider 
from scrapy.selector import Selector
from scrapy.http import Request
from Movie.items import MovieInformation
import re

class MovieSpider(Spider):
    name = "movieinformation"
    start_urls = [
        'https://movie.douban.com/tag/'
    ]

    def parse(self, response):
#    def test(self, response):
        selector = Selector(response)
        urls = selector.xpath('//table[last()]/tbody/tr/td/a/@href').extract()
        for raw_url in map(lambda url: url.replace('www', 'movie'), urls):
            url = re.sub(r'/\?', '?', raw_url) # 防止重定向
            yield Request(url=url, callback=self.movieParse)
            
    def movieParse(self, response):
    #def parse(self, response):
        selector = Selector(response)
        movie_urls = selector.xpath('//td[@valign="top"]/div/a/@href').extract()
        for url in movie_urls:
            yield Request(url=url, callback=self.informationParse)
        next_page = selector.xpath('//*[@id="content"]/div/div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if next_page:
            yield Request(url=next_page[0], callback=self.movieParse)
    
    def informationParse(self, response):
        information = MovieInformation()
        selector = Selector(response)
        information['id'] = re.findall(r'([\d]+)', response.url)
        information['year'] = selector.xpath('//*[@id="content"]/h1/span[@class="year"]/text()').extract()
        information['movie'] = selector.xpath('//*[@id="content"]/h1/span[@property="v:itemreviewed"]/text()').extract()
        # 取消[@id="info"]后span的绝对定位，并非所有电影都有导演、编剧、主演
        information['director'] = selector.xpath('//*[@id="info"]/span/span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()        
        information['writer'] = selector.xpath('//*[@id="info"]/span/span[@class="attrs"]/a[not(@rel)]/text()').extract()
        information['actor'] = selector.xpath('//*[@id="info"]/span/span[@class="attrs"]/a[@rel="v:starring"]/text()').extract()
        information['type'] = selector.xpath('//*[@id="info"]/span[@property="v:genre"]/text()').extract()
        information['official_site'] = selector.re(r'<span[\s]+class="pl">官方网站[\W]+</span>[\s]+<a[\s]+href="(.*?)"')
        # information['official_site'] = selector.xpath('//*[@id="info"]/a[@target="_blank" and @rel="nofollow"]').re(r'href="(((?!imdb)[\S])*)"') 有缺陷的正则
        information['area'] = selector.re(r'<span[\s]+class="pl">制片国家/地区[\W]+</span>(.*?)<br')
        information['language'] = selector.re(r'<span[\s]+class="pl">语言[\W]+</span>(.*?)<br')
        information['release_data'] = selector.xpath('//*[@id="info"]/span[@property="v:initialReleaseDate"]/@content').extract()
        # 连续剧内容 
        information['season'] = selector.xpath('//*[@id="season"]/option[@selected="selected"]/text()').extract()
        information['episodes'] = selector.re(r'<span[\s]+class="pl">集数[\W]+</span>(.*?)<br')
        information['single_runtime'] = selector.re(r'<span[\s]+class="pl">单集片长[\W]+</span>(.*?)<br')
        # end
        information['runtime'] = selector.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content').extract() # 仅提取一个时间
        information['alias'] = selector.re(r'<span[\s]+class="pl">又名[\W]+</span>(.*?)<br')
        information['imdb'] = selector.xpath('//*[@id="info"]/a[@target="_blank" and @rel="nofollow"]').re(r'href="([\S]+\.\bimdb\b\.[\S]+)"') # re(r'href="([\S]+\.imdb\.[\S]+)"') re(r'href="([\S]+imdb[\S]+)"')
        information['synopsis'] = selector.xpath('//*[@id="link-report"]//span[@property="v:summary"]/text()').extract() # 相对定位，解决<span>嵌套问题
        awards_url = selector.css('#content > div > div.article > div.mod > div > h2 > span > a::attr(href)').extract()
        if awards_url:
            yield Request(url=awards_url[0], meta={'info': information}, callback=self.awardsParse)
        else:
            yield information

    def awardsParse(self, response):
        information = response.meta['info']
        information['awards'] = list()
        selector = Selector(response)
        items = selector.css('#content > div > div.article > div.awards')
        for item in items:
            awards = dict()
            awards['name'] = item.css('div > h2 > a::text').extract()
            awards['year'] = item.css('div > h2 > span::text').extract()
            awards['items'] = list()
            for ul in item.css('ul'):
                title = ul.css('li:nth-child(1)::text').extract()
                people = ul.css('li:nth-child(2) > a::text').extract()
                awards['items'].append(dict(title=title, people=people))
            information['awards'].append(awards)
        yield information
