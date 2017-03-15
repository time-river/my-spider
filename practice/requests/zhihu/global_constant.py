#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
此文件定义全局常量
'''

zhihu_url = 'https://www.zhihu.com'
login_url = zhihu_url + '/login/email'
captcha_url_prefix = zhihu_url + '/captcha.gif?r='

#获取话题的相关常量
default_root= "https://www.zhihu.com/topic/19776749/organize/entire"
#headers
headers = {
    'Host': "www.zhihu.com",
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0",
    'Referer': "https://www.zhihu.com/"
}
