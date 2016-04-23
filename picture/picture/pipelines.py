# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pickle
import redis
from picture.items import PictureItem

class PicturePipeline(object):
    def __init__(self):
        self.redis = redis.StrictRedis("127.0.0.1")

    def process_item(self, item, spider):
        self.redis.lpush("picture", pickle.dumps(item)
        return item
