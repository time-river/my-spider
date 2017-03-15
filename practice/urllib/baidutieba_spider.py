#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
from http://cuiqingcai.com/993.html
I just copy it and use python3 to rewrite it.
'''

import urllib.request
import urllib.parse
import urllib.error
import re

class Tool:
    '''
    除去页面标签
    '''
    def __init__(self):
        self.removeImg = re.compile(r'<img.*?>| {7}') #删除 img标签 或 7位长空格
        self.removeAddr = re.compile(r'<a.*?>|</a>') #删除 超链接标签
        self.replaceLine = re.compile(r'<br><br>|<br>|<tr>|<div>|</div>|</p>') #换行的标签 置为 \n
        self.replaceTD = re.compile(r'<td>')  #td标签 换为 \t
        self.replacePara = re.compile(r'<p.*?>') #段落开头加空格
        self.removeExtraTag = re.compile(r'<.*?>') #移除其他标签
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

class BDTB:
    '''
    百度贴吧爬虫
    '''
    def __init__(self, baseUrl, seeLZ, floorTag):
        '''
        传入参数
        baseURL, seeLZ, floorTag
        初始化参数
        baseUrl: 百度贴吧某一资源
        seeLZ：布尔值，取0或1，含义——是否只看楼主
        file：文件写入变量
        floor：楼层标号，初始为1
        defaultTitle：默认标题，未获取标题则使用此标题
        floorTag：是否写入楼层分隔符号标记
        '''
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.file = None
        self.floor = 1
        self.defaultTitle = "百度贴吧"
        self.floorTag = floorTag
        self.tool = Tool()

    def getPage(self, pageNum):
        '''
        功能
        获取制定页码的html文档
        传入参数
        pageNum：传入页码
        '''
        try:
            url = self.baseURL+ self.seeLZ + '&pn=' + str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request, timeout=30)
            page = response.read().decode("utf-8")
            return page
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print("We failed to reach a server. Please check your url and read the reason")
                print("Reason: {}".format(e.reason))
                return None
            elif hasattr(e, "code"):
                print("The server couldn't fulfill the request.")
                print("Error code: {}".format(e.code))
                return None

    def getTitle(self, page):
        '''
        功能
        获取帖子标题
        传入参数
        page：获取到的html文档
        '''
        pattern = re.compile(r'<h\d.*?class="core_title_txt.*?>(.*?)</h\d>')
        result = pattern.search(page)
        if result:
            return result.group(1).strip()
        #为了使用正则表达式匹配到的这些分组，需要对search()函数的返回值调用groups()方法。它会返回一个这个正则表达式中定义的所有分组结果组成的元组。
        else:
            return None

    def getPageNum(self, page):
        '''
        功能
        获取帖子页数
        传入参数
        page：获取到的html文档
        '''
        pattern = re.compile(r'<a.*?href=".*?pn=(\d+)">尾页</a>')
        number = pattern.search(page)
        if number:
            return number.group(1).strip()
        else:
            return None

    def getContents(self, page):
        '''
        功能
        提取百度贴吧每层楼内容
        传入参数
        page：获取到的html文档
        '''
        pattern = re.compile(r'<div.*?id="post_content.*?>(.*?)</div>', re.S)
        items = pattern.findall(page)
        try:
            contents = []
            for item in items:
                content = "\n" + self.tool.replace(item) + "\n"
                contents.append(content)
            return contents
        except TypeError as e:
            print("未找到内容")

    def setFileTitle(self, title):
        '''
        功能
        设置文件名称
        传入参数
        title：获取到的帖子标题
        '''
        if title is not None:
            return title
        else:
            return self.defaultTitle

    def writeData(self, title, contents):
        '''
        功能
        向文件中写入每层楼信息
        参数
        title:帖子标题
        contents:楼层信息
        '''
        for item in contents:
            with open(title+".txt", "a") as file:
                if self.floorTag == '1':
                    floorLine = "\n" + str(self.floor) + "-----------------------------------------------------------------------------------------\n"
                    file.write(floorLine)
                file.write(item)
                self.floor += 1

    def start(self):
        page = self.getPage(1)
        pageNum = self.getPageNum(page)
        title = self.getTitle(page)
        fileTitle = self.setFileTitle(title)
        if pageNum is None:
            print("链接已经失效")
            return
        try:
            print("该帖子共有{}页".format(pageNum))
            for i in range(1, int(pageNum)+1):
                print("正在写入第{}页数据".format(i))
                page = self.getPage(i)
                contents = self.getContents(page)
                self.writeData(fileTitle, contents)
        except IOError as e:
            print("写入异常，原因{}".format(e.code))
        finally:
            print("写入完成")

baseURL = 'http://tieba.baidu.com/p/3138733512'
seeLZ = 1
floorTag = 1
spider = BDTB(baseURL, seeLZ, floorTag)
spider.start()
