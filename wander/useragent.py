#!/usr/bin/env python
# -*- coding:utf-8 =*-

import redis
from base import redis_sadd, redis_info

def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    ua_list = list()
    with open('UA.txt') as f:
        for line in f.readlines():
            ua_list.append(line.strip())
    redis_sadd(r, 'user.agent', ua_list)


if __name__ == '__main__':
    main()