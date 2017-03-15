#!/usr/bin/env python3
#-*- coding:utf-8 -*-

'''
from http://cuiqingcai.com/990.html
I just copy it and use python3 to rewrite.
'''
import urllib
import urllib.request
import urllib.error
import re
import time

class QSBK:
    '''
    糗事百科爬虫
    '''
    def __init__(self):
        '''
        初始化变量:
            pageIndex: 当前页面
            headers: request headers
            stories: 存放段子的变量
            enable: 控制程序是否继续运行
        '''
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36"
        self.headers = { 'User-Agent' : self.user_agent }
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        '''
        获取html文档
        '''
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            request = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(request)
            content = response.read().decode("utf-8")
            return content
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print("服务器无应答, 代码: {}".format(e.code))
            if hasattr(e, "reason"):
                print("糗事百科连接失败, 错误: {}".format(e.code))
            return None

    def getPageItems(self, pageIndex):
        '''
        解析html文档，正则匹配段子
        '''
        content = self.getPage(pageIndex)
        if not content:
            print("页面加载失败")
            return None
        pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?href.*?title="(.*?)">.*?</a>.*?<div.*?class="content">(.*?)<!--.*?</div>.*?<div.*?class="stats.*?<i.*?class="number">(.*?)</i>', re.S)
        items = re.findall(pattern, content)
        pageStories = []
        for item in items:
            info = []
            for index in item:
                info.append(index.strip())
            info.append(time.strftime("%Y-%m-%d %H:%M:%S")) #时间
            pageStories.append(info)
        return pageStories

    def loadPage(self):
        '''
        加载页面内容，并获取到列表中
        '''
        if self.enable == True:
            if len(self.stories) < 2: #如果当前未看的页数少于两页，则加载新的页面，即执行getPageItems()方法
                    pageStories = self.getPageItems(self.pageIndex)
                    if pageStories:
                        self.stories.append(pageStories)
                        self.pageIndex += 1

    def getOneStory(self, pageStories, page):
        '''
        获取一个段子
        '''
        for story in pageStories:
            tag = input()
            self.loadPage()
            if tag is "Q":
                self.enable = False
                return None
            print ("第{0}页\t发布人:{1}\t时间:{2}\t赞:{3}\n{4}".format(page,story[0],story[3],story[2],story[1]))

    def start(self):
        print("正在读取糗事百科，按回车查看新段子，Q退出")
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0] #删除全局list中的第一个元素，因为已经取出
                self.getOneStory(pageStories, nowPage)

spider = QSBK()
spider.start()
