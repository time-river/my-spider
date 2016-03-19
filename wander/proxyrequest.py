#!/usr/bin/env python
# -*- coding:utf-8 -*-

from configparser import ConfigParser
from base import redis_push
import redis

def get_raw_proxy():
    lst = list()
    cfg = ConfigParser()
    cfg.read('config.ini')
    items = cfg.sections()
    for item in items:
        lst.append((
            cfg.get(item, 'order'),
            cfg.get(item, 'url'),
            cfg.get(item, 'number')
        ))
    return lst

def main():
    r = redis.StrictRedis(host='127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")
    request_list = list()
    for item in get_raw_proxy():
        for i in range(int(item[2])):
            request_list.append({
            'url': '{}{}'.format(item[1], i+1),
            'params': None,
            'headers': None,
            'type': 'utf-8',
            'order': item[0]
            })
    redis_push(r, 'proxy.request', request_list)

if __name__ == '__main__':
    print('----------raw_proxy_request start----------')
    main()
    print('----------raw_proxy_request end----------')