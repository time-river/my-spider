#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import proxy

def main(params=None):
    r = redis.StrictRedis(host='127.0.0.1', password='d41d8cd98f00b204e9800998ecf8427e')
    verifier = proxy.Proxy(redis=r, raw_proxy_key="raw.proxy", proxy_key="proxy")
    if params == 'monitor':
        print('start')
        verifier.monitor()
    else:
        verifier.main()
    
if __name__ == '__main__':
    main('monitor')
    #main()