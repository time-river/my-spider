#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import redis_push, items_info, redis_info, redis_srandmember
import redis

URL = "https://www.douban.com/tag/2014/movie"

def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    request_list = list()
    for i in range(0, 510, 15):
        request_list.append({
        'url': URL,
        'params': {
            'start': repr(i)
        },
        'headers': {
            "Host": "www.douban.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            'User-Agent': redis_srandmember(r, 'user.agent')
        },
        'type': 'utf-8',
        'order': 'douban'
        })
    redis_push(r, 'douban.movie.request', request_list)

if __name__ == '__main__':
    main()
