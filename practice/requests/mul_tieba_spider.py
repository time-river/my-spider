#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
涉及知识:
Requests 获取网页内容
XPath提取内容
map实现多线程爬虫
'''

from lxml import etree
from multiprocessing import Pool as ThreadPool
import requests
import json
import time

def towrite(content_dict):
    with open('content.txt', 'a') as f:
        f.writelines("回帖时间：{}\n".format(content_dict['topic_reply_time']))
        f.writelines("回帖内容：{}\n".format(content_dict['topic_reply_content']))
        f.writelines("回帖人：  {}\n\n".format(content_dict['user_name']))

def spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[starts-with(@class, "l_post j_l_post l_post_bright")]')
    item = dict()
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0])
        author = reply_info['author']['user_name']
        reply_time = reply_info['content']['date']
        print(author, reply_time)
        content = each.xpath('div[starts-with(@class, "d_post_content_main")]/div/cc/div[@class="d_post_content j_d_post_content  clearfix"]')[0].xpath('string(.)').strip()
        print(content)
        item['user_name'] = author
        item['topic_reply_content'] = content
        item['topic_reply_time'] = reply_time
        towrite(item)

if __name__ == '__main__':
    pool = ThreadPool(32)
    page = list()
    for i in range(1, 696):
        newpage = 'http://tieba.baidu.com/p/3522395718?pn=' + str(i)
        page.append(newpage)
    time_start = time.time()
    results = pool.map(spider, page)
    pool.close()
    pool.join()
    time_end = time.time()
    print("抓取695页耗时：{}".format(time_end-time_start))
