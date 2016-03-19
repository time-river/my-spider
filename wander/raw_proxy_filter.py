#!/usr/bin/env python
# -*- coding:utf-8 -*-

from filter import Filter # recommend, avoid a conflict of `filter()`
import redis
import re
# http://www.mimiip.com/gngao/
def ip84_filter(content):
    data = list()
    pattern = re.compile(r'<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?<td>(.*?)</td>.*?<td>.*?</td>.*?<td>.*?</td>.*?</tr>', re.S)
    raw_data = pattern.findall(content)
    for raw in raw_data:
        item = list(map(lambda word: word.lower(), raw))
        data.append({'ip': item[0], 'port': item[1], 'protocol': item[2]})
    return data # 'proxy' is the key of redis
    
def main():
    r = redis.StrictRedis(host='127.0.0.1', password='d41d8cd98f00b204e9800998ecf8427e')
    filters = Filter(ip84_filter, redis=r, content_key="proxy_content")
    filters.main()
    
if __name__ == '__main__':
    main()