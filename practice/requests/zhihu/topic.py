#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
获取知乎话题部分
'''

import bs4
import time
import pickle
import authentication
from global_constant import *

class Topic(object):
    '''
    获取话题
    '''
    def __init__(self, session, root=None):
        '''

        '''
        if root is None:
            self._root = default_root #若root_url给定，则从root_url开始遍历，否则从知乎根结点开始遍历
        else:
            self._root = root
        self._session = session
        self._session.headers.update({
            'X-Requested-With': "XMLHttpRequest",
            'Referer': "https://www.zhihu.com/topic/19776749/organize/entire"
        })
        self._queue = list() #利用list实现先进先出队列
        self.time = 0

    def BFS_travel(self):
        '''
        通过图的广度优先搜索获取JSON数据
        '''
        root_url = self._root
        self._handle(url=root_url)
        while(self._queue):
            topic = self._queue.pop(0)
            parent = topic[3]
            self._handle(url=root_url, parent=parent)
        print("抓取完成!")

    def _handle(self, **kw):
        loads_list = [False]
        url = kw['url']
        if 'child' in kw:
            child = kw['child']
        else:
            child = ""
        if 'parent' in kw:
            parent = kw['parent']
        else:
            parent = ""
        form_data = {
            '_xsrf': self._session.cookies.get('_xsrf')
        }
        while loads_list: #[]为False
            load = loads_list.pop(0)
            if load: #判断是否为第一次循环，第一次循环load值False
                child = load[2]
                parent= load[3]
            params = self._get_params(child, parent)
            self.time += 1
            if self.time % 10000 == 0:
                time.sleep(30)
            print(self.time)
            try:
                response = self._session.post(url, params=params, data=form_data)
                topic_list, loads_list = self._filter_response(response.json())
                with open('topic.txt', 'a') as f:
                    f.write(str(self.time)+'\n')
                for topic in topic_list:
                    print(topic)
                    with open("topic.txt", 'a') as f:
                        f.write(str(topic)+'\n')
                    if topic[0]:
                        self._queue.append(topic)
            except:
                print("Error");
                time.sleep(60)
                if load:
                    loads_list.insert(0, load)
                else:
                    self._queue.insert(0, [True, 'topic', child, parent])

    def _save_topic(self, tmp):
        with open('topic.txt', 'w') as f:
            pickle.dump(tmp, f)

    def _filter_response(self, json):
        '''
        处理JSON数据
        JSON数据格式
        键                      值
        json['r']               0
        json['msg']            话题

        列表对象                含义
        json['msg'][0]         父话题
        json['msg'][1]         子话题列表
        json['msg'][1][n]      第n个子话题
        json['msg'][1][n][0]   ['topic', 话题名称, 话题编号] 或 ['load', '加载更多', child, parent]
        json['msg'][1][n][1]   [[['load', '显示子话题', '', parent], []]] 或 []

        返回的数据格式
        topic_list             话题列表
        topic_list[n]          [判断是否入队的布尔值, 'topic', 话题名称, 话题编号]
        loads_list             ['load', '加载更多', child, parent]
        '''
        raw_data = json['msg'][1]
        topic_list = list()
        loads_list = list()
        for item in raw_data:
            if item[0][0] == 'load':
                loads_list.append(item[0])
            else:
                if item[1] == []: #不存在子话题
                    item[0].insert(0, False)
                else:
                    item[0].insert(0, True)
                topic_list.append(item[0])
        return topic_list, loads_list

    def _get_params(self, child, parent):
        '''
        获取的查询字符串
        3种查询情况
        '''
        if parent is "":
            return None
        else:
            params = {
                'child': child,
                'parent': parent
            }
            return params

import authentication
kw = {
'email': 'feather12315@live.com',
'password': 'feather12315'
}
session = authentication.Authentication(kw=kw)
spider = Topic(session.session)
spider.BFS_travel()
