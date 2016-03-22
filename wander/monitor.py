#!/usr/bin/env python
# -*- coding:utf-8 -*-

from base import redis_info
import redis
import subprocess
import time
import os

def setup():
    sub = subprocess.Popen(['python3.5', 'useragent.py'])
    sub.wait()
    subs = [subprocess.Popen(['python3.5', 'proxyrequest.py'])]
    subs.append(subprocess.Popen(['python3.5', 'proxyclaw.py']))
    subs.append(subprocess.Popen(['python3.5', 'proxyfilter.py']))
    subs.append(subprocess.Popen(['python3.5', 'proxyverify.py']))
    for sub in subs:
        sub.wait()

def main():
    info = redis_info()
    r = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
    setup()
    endure = subprocess.Popen(['python3.5', 'proxymonitor.py'])
    pid = endure.pid
    while True:
        time.sleep(600)
        if r.scard('proxy') < 500:
            setup()
        if not(os.path.exists(pid)):
            subprocess.Popen(['python3.5', 'proxymonitor.py'])
            pid = endure.pid
            
if __name__ == "__main__":
    main()
           
