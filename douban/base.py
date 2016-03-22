#!/usr/bin/env python
# -*- coding:utf-8 -*-

from configparser import ConfigParser
from functools import wraps
import pickle
import logging

def get_log(name=None):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
    
def redis_login():
    cfg = ConfigParser()
    cfg.read('config.ini')
    info = {
        'host': cfg.get('redis', 'host'),
        'port': cfg.getint('redis', 'port'),
        'password': cfg.get('redis', 'password')
    }
    return info
    
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
def rpush(redis, key, objects):
    for obj in objects:
        redis.rpush(key, obj)
    
def blpop(redis, key, timeout=30):
    serialization = redis.blpop(key, timeout=timeout)
    if serialization:
        return pickle.loads(serialization[1])
        
# set operation
@push
def sadd(redis, key, objects):
    for obj in objects:
        redis.sadd(key, obj)

def srandmember(redis, key):
    serialization = redis.srandmember(key)
    if serialization:
        return pickle.loads(serialization)