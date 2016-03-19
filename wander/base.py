#!/usr/bin/env python
# -*- coding:utf-8 -*-

from configparser import ConfigParser
from functools import wraps
import pickle

def redis_info():
    cfg = ConfigParser()
    cfg.read('config.ini')
    info = {
        'host': cfg.get('redis', 'host'),
        'port': cfg.getint('redis', 'port'),
        'password': cfg.get('redis', 'password')
    }
    return info

def items_info(cfg):
    items = cfg.sections()
    items.remove('redis')
    return items
       
def push(func):
    @wraps(func)
    def dec(redis, key, objects):
        if not (isinstance(objects, tuple) or isinstance(objects, list)):
            objects = [objects]
        serialization = list()
        for obj in objects:
            serialization.append(pickle.dumps(obj))
        pipe = redis.pipeline()
        func(pipe, key, serialization)
        pipe.execute()
    return dec

# list operation
@push
def redis_push(redis, key, objects):
    for obj in objects:
        redis.rpush(key, obj)
    
def redis_pop(redis, key, timeout=600):
    serialization = redis.blpop(key, timeout=timeout)
    if serialization:
        return pickle.loads(serialization[1])

def redis_rpoplpush(redis, r_key, l_key):
    serialization = redis.rpoplpush(r_key, l_key)
    if serialization:
        return pickle.loads(serialization)

# set operation
@push
def redis_sadd(redis, key, objects):
    for obj in objects:
        redis.sadd(key, obj)

def redis_srandmember(redis, key):
    serialization = redis.srandmember(key)
    if serialization:
        return pickle.loads(serialization)

def redis_srem(redis, key, obj):
    serialization = pickle.dumps(obj)
    print(redis.srem(key, serialization))
    
def redis_smembers(redis, key):
    objects = list()
    serializations = redis.smembers(key)
    for serialization in serializations:
        objects.append(pickle.loads(serialization))
    return objects