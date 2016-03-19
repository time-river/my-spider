#!/usr/bin/env python
# -*- coding:utf-8 -*-

from configparser import ConfigParser
from base import redis_push, items_info, redis_info, redis_srandmember
import redis

def get_raw_proxy():
    lst = list()
    cfg = ConfigParser()
    cfg.read('config.ini')
    items = items_info(cfg)
    for item in items:
        lst.append((
            cfg.get(item, 'order'),
            cfg.get(item, 'url'),
            cfg.get(item, 'number')
        ))
    return lst

def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    request_list = list()
    for item in get_raw_proxy():
        for i in range(int(item[2])):
            request_list.append({
            'url': '{}{}'.format(item[1], i+1),
            'params': None,
            'headers': {
                'User-Agent': redis_srandmember(r, 'user.agent')
            },
            'type': 'utf-8',
            'order': item[0]
            })
    redis_push(r, 'proxy.request', request_list)

if __name__ == '__main__':
    main()