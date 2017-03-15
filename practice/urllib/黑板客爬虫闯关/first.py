#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "time-river"

'''
爬虫闯关第一关 http://www.heibanke.com/lesson/crawler_ex00/
提示技能: 打开网页，下载文件：urllib
来自 http://www.zhihu.com/question/20899988 黑板客的回答
'''

import urllib
from urllib import request
from urllib import error
import re

class first:
    '''
    爬虫闯关第一关代码
    思路:
    分析url
    爬取html文档
    获取提示信息
    拼接url并继续爬取，直至无提示信息
    '''
    def __init__(self):
        self.base_url = "http://www.heibanke.com/lesson/crawler_ex00/"

    def get_page(self, prompt):
        try:
            url = self.base_url + prompt
            response = request.urlopen(url)
            #获取charset，有时charset并不是utf-8
            content_type = response.headers.get("content-type")
            pattern = re.compile(r"charset=(.*)$")
            charset = pattern.findall(content_type)
            page = response.read().decode(str(charset))
            return page
        except error.URLError as e:
            if hasattr(e, "reason"):
                print ("We failed to reach a server. Please check your url and read the Reason")
                print ("Reason: {}".format(e.reason))
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: {}".format(e.code))
            return
    def get_prompt(self, page):
        pattern = re.compile(r"<h.*?数字\D*?(\d{5}).*?</h\d>")
        prompt = pattern.search(page)
        if prompt:
            return prompt.group(1)
        else:
            return None

    def solution(self):
        tag = True
        prompt = ''
        while(tag):
            page = self.get_page(prompt)
            prompt = self.get_prompt(page)
            print(prompt)
            if not prompt:
                tag = False
        print(page)

spider = first()
spider.solution()
