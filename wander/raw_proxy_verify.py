#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis
import proxy

def main():
    r = redis.StrictRedis(host='127.0.0.1', password='d41d8cd98f00b204e9800998ecf8427e')
    verifier = proxy.Proxy('https://movie.douban.com', redis=r, raw_proxy_key="raw_proxy", proxy_key="proxy")
    verifier.main()
    
if __name__ == '__main__':
    main()
