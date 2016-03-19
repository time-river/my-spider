#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import redis_push
import redis

def main():
    r = redis.StrictRedis(host='127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")
    request_list = list()
    for i in range(1, 101):
        request_list.append({
            'url': 'http://www.ip84.com/gn-http/{}'.format(i),
            'params': None,
            'headers': None,
            'type': 'utf-8'})
    redis_push(r, 'proxy_request', request_list)

if __name__ == '__main__':
    print('----------raw_proxy_request start----------')
    main()
    print('----------raw_proxy_request end----------')
