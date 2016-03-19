#!/usr/bin/env python
# -*- coding:utf-8 =*-

import redis
from base import redis_sadd
import time
def main():
    r = redis.StrictRedis(host='127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")
    ua_list = list()
    with open('UA.txt') as f:
        for line in f.readlines():
            ua_list.append(line.strip())
    redis_sadd(r, 'User-Agent', ua_list)


if __name__ == '__main__':
    print('**********start**********')
    main()
    print('**********end**********')
