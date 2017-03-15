#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "time-river"

'''
爬虫闯关第一关 http://www.heibanke.com/lesson/crawler_ex01/
提示技能：post方法、表单登陆
来自 http://www.zhihu.com/question/20899988 黑板客的回答
'''

from urllib import request
from urllib import parse
from urllib import error
import re

class second:
    def __init__(self):
        self.name = "second"
        self.url = "http://www.heibanke.com/lesson/crawler_ex01/"

    def guess(self):
        for i in range(31):
            print("正在猜测密码为{}".format(i))
            form = {
                "username": self.name,
                "password": i
            }
            data = parse.urlencode(form).encode('utf-8')
            req = request.Request(self.url, data)
            try:
                with request.urlopen(req) as f:
                    body = f.read().decode("utf-8")
                    if not "您输入的密码错误, 请重新输入" in body:
                        print(body)
                        print("密码为{}".format(i))
                        break
            except error.URLError as e:
                if hasattr(e, "reason"):
                    print ("We failed to reach a server. Please check your url and read the Reason")
                    print ("Reason: {}".format(e.reason))
                elif hasattr(e, "code"):
                    print("The server couldn't fulfill the request.")
                    print("Error code: {}".format(e.code))
                return

spider = second()
spider.guess()
