# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pickle
import redis

class MoviePipeline(object):
    def __init__(self):
        self.redis = redis.StrictRedis('127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")

    def process_item(self, item, spider):
        item = information_filter(item)
        data = dict(item)
        self.redis.rpush('test.movie.information', pickle.dumps(data))
        return item

    @staticmethod
    def information_filter(item):
        if item['year']:
            item['year'] = item['year'][0].strip('() ')
        if item['area']:
            item['area'] = item['area'][0].replace('/', ' ').split()
        if item['language']:
            item['language'] = item['language'][0].replace('/', ' ').split()
        if item['alias']:
            item['alias'] = item['alias'][0].replace('/', ' ').split()
        if item['synopsis']:
            item['synopsis'] = list(map(lambda string: string.strip(), item['synopsis']))
        if item['awards']:
            def award_filter(obj):
                obj['year'] = obj['year'][0].strip('() ')
                return obj
            item['awards'] = list(map(award_filter, item['awards']))
        return item
