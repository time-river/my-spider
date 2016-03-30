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
        data = dict(item)
        self.redis.rpush('movie', pickle.dumps(data))
        return item
