# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pickle
import redis
from Movie.items import MovieInformation

def list_ss(obj, *, ch=None, ar=None):
    '''
    list split and strip
    '''
    objects = list()
    if not isinstance(obj ,list):
        obj = [obj]
    if ar:
        for item in obj:
            objects.extend(item.split(ar))
    else:
        objects = obj
    results = list(map(lambda x: x.strip(ch), objects))
    return results 

def information_filter(item):
    # id movie director writer actor type official_site release_data
    info = MovieInformation()
    if item['id']:
        info['id'] = list_ss(item['id'])
    if item['year']:
        info['year'] = list_ss(item['year'], ch='() ')
    if item['movie']:
        info['movie'] = list_ss(item['movie'])
    if item['director']:
        info['director'] = list_ss(item['director'])
    if item['writer']:
        info['writer'] = list_ss(item['writer'])
    if item['actor']:
        info['actor'] = list_ss(item['actor'])
    if item['type']:
        info['type'] = list_ss(item['type'])
    if item['official_site']:
        info['official_site'] = list_ss(item['official_site'])
    if item['area']:
        info['area'] = list_ss(item['area'], ar='/')
    if item['language']:
        info['language'] = list_ss(item['language'], ar='/')
    if item['release_data']:
        info['release_data'] = list_ss(item['release_data'])
    if item['season']:
        info['season'] = list_ss(item['season'])
    if item['episodes']:
        info['episodes'] = list_ss(['episodes'])
    if item['single_runtime']:
        info['single_runtime'] = list_ss(item['single_runtime'])
    if item['alias']:
        info['alias'] = list_ss(item['alias'], ar='/')
    if item['imdb']:
        info['imdb'] = list_ss(item['imdb'])
    if item['synopsis']:
        info['synopsis'] = list_ss(item['synopsis'])
    if item['awards']:
        def award_filter(obj):
            obj['year'] = list_ss(obj['year'], ch=' ()\xa0')
            return obj
        info['awards'] = list(map(award_filter, item['awards']))
    return info

class MoviePipeline(object):
    def __init__(self):
        self.redis = redis.StrictRedis('127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")

    def process_item(self, item, spider):
        item = information_filter(item)
        data = dict(item)
        self.redis.rpush('test', pickle.dumps(data))
        return item
