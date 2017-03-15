#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
参考 https://github.com/7sDream/zhihu-py3/blob/master/zhihu/client.py

知乎认证部分
'''

import os
import time
import json
import requests
from PIL import Image
from global_constant import *

class Authentication(object):
    '''
    知乎认证类，可用cookies(JSON数据格式)或者帐号密码登陆
    若使用帐号密码登陆，则会将cookies以JSON数据格式保存至当前文件夹下
    '''
    def __init__(self, cookies_path=None, kw=None):
        self.session = requests.Session()
        self.session.headers.update(headers)
        if cookies_path is not None:
            assert isinstance(cookies_path, str)
            self._login_with_cookies(cookies_path)
        elif kw is not None:
            self._login_with_email(kw)
        else:
            print("Input the parameter.")

    def _login_with_cookies(self, cookies_path):
        '''
        使用cookies文件登陆
        cookies_path：cookie文件路径
        cookies是JSON数据格式
        '''
        try:
            with open(cookies_path) as f:
                cookies = f.read()
            self.session.cookies.update(json.loads(cookies))
        except FileNotFoundError as e:
            print("No such file or directory.")

    def _login_with_email(self, kw):
        '''
        使用帐号密码登陆
        登陆过程：
            请求 url: https://www.zhihu.com
            获取 _xsrf
            请求 url: https://www.zhihu.com/captcha.gif?r=*
            获取 captcha.gif
            手动输入 captcha
            登陆
        kw：帐号、密码字典
        '''
        xsrf = self._get_xsrf()
        captcha = self._get_captcha()
        form_data = {
            '_xsrf': xsrf,
            'captcha': captcha,
            'remember_me': 'true'
        }
        form_data.update(kw)
        response = self.session.post(login_url, data=form_data)
        if response.status_code is 200:
            print("Login sucessfully.")
            self._save_cookies()
        else:
            print("Login failed.")

    def _get_xsrf(self):
        self.session.get(zhihu_url)
        return self.session.cookies.get('_xsrf')

    def _get_captcha(self):
        captcha_url = captcha_url_prefix + str(int(time.time() * 1000))
        response = self.session.get(captcha_url)
        with open("captcha.gif", 'wb') as f:
            for i in response:
                f.write(i)
        with open("captcha.gif", 'rb') as f:
            Image.open(f).show()
        os.remove("captcha.gif")
        return input("Input the captcha.\n")

    def _save_cookies(self):
        '''
        保存cookies至当前文件夹下
        '''
        with open('cookies.json', 'w') as f:
            json.dump(self.session.cookies.get_dict(), f)

    def set_proxy(self, proxy):
        '''
        设置代理
        proxy: str, 形式： "('http', 'example.com:port')"
        '''
        self.session.proxies.update({proxy[0]+'://': proxy[1]})
