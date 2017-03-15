#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import proxy
from base import redis_info


def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    verifier = proxy.Proxy(redis=r, raw_proxy_key="raw.proxy", proxy_key="proxy")
    verifier.monitor()
    
if __name__ == '__main__':
    main()