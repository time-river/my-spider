#!/usr/bin/env python
# -*- coding:utf-8 -*

from scrapy.contrib.spiders import Spider 
from scrapy.selector import Selector
from scrapy.http import Request
from Movie.items import MovieReview, MovieReviewComment

class ReviewSpider(Spider):
    name = "moviereview"

    def parse(self, response):
        selector = Selector(response)

