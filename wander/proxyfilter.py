#!/usr/bin/env python
# -*- coding:utf-8 -*-

from configparser import ConfigParser
from filter import Filter # recommend, avoid a conflict of `filter()`
import redis
import re

# http://www.mimiip.com/gngao/

def filter_rule():
    rules = dict()
    cfg = ConfigParser()
    cfg.read('config.ini')
    items = cfg.sections()
    for item in items:
        rules[cfg.get(item, 'order')] = cfg.get(item, 'rule')
    return rules
    
def filt(content, rule):
    data = list()
    #pattern = re.compile(r'<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?</tr>', re.S)
    pattern = re.compile(rule, re.S)
    raw_data = pattern.findall(content)
    for raw in raw_data:
        item = list(map(lambda word: word.lower(), raw))
        data.append({'ip': item[0], 'port': item[1], 'protocol': item[2]})
    return data
    
def main():
    r = redis.StrictRedis(host='127.0.0.1', password='d41d8cd98f00b204e9800998ecf8427e')
    filters = Filter(filt, filter_rule(), redis=r, content_key="proxy.content", raw_proxy_key='raw.proxy')
    filters.main()
    
if __name__ == '__main__':
    main()