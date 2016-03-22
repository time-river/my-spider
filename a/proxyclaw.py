#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import claw
from base import redis_info

def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    clawer = claw.Claw(redis=r, request_key='proxy.request', content_key="proxy.content")
    clawer.main()

if __name__ == '__main__':
    main()