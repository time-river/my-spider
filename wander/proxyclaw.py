#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import claw

def main():
    r = redis.StrictRedis(host='127.0.0.1', password="d41d8cd98f00b204e9800998ecf8427e")
    clawer = claw.Claw(redis=r, request_key='proxy.request', content_key="proxy.content")
    clawer.main()

if __name__ == '__main__':
    main()