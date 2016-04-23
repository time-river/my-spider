#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import pickle

if __name__ == '__main__':
    r = redis.StrictRedis()
    one = r.rpop('picture')
    item = pickle.loads(one)
    with open('example.jpg', 'wb') as f:
        f.write(item['picture'])
