#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import logging
import requests
from lxml import etree
import redis
import base
import time
from PIL import Image
import re
import os


    
class Download:
    def __init__(self):
        info = base.redis_login()
        self.redis = redis.StrictRedis(host=info['host'], port=info['port'], password=info['password'])
        self.logger = base.get_log(name="download")
        self.session = requests.Session()
        self.comments_num = 0
        self.max_comments = 0
        self._get_session()
        
    def _get_session(self):
        try:
            response = self.session.get('https://www.douban.com/accounts/login', timeout=10)
            try:
                assert response.status_code == 200
                selector = etree.HTML(response.text)
                data = {
                        selector.xpath('//*[@id="lzform"]/input[2]/@name')[0]:
                            selector.xpath('//*[@id="lzform"]/input[2]/@value')[0],
                        selector.xpath('//*[@id="lzform"]/input[1]/@name')[0]:
                            selector.xpath('//*[@id="lzform"]/input[1]/@value')[0],
                        selector.xpath('//*[@id="email"]/@name')[0]:
                            'feather12315@163.com',
                        selector.xpath('//*[@id="password"]/@name')[0]:
                            'dou12315ban',
                        selector.xpath('//*[@id="lzform"]/div[@class="item"]/input[@type="submit"]/@name')[0]:
                            selector.xpath('//*[@id="lzform"]/div[@class="item"]/input[@type="submit"]/@value')[0],
                        selector.xpath('//*[@id="remember"]/@name')[0]:
                            'on'
                }
                print(data)
                if selector.xpath('//*[@id="captcha_image"]'):
                    value = self._get_captcha(selector.xpath('//*[@id="captcha_image"]/@src')[0])
                    data[selector.xpath('//*[@id="lzform"]/div[5]/div/div/input[2]/@name')[0]] = selector.xpath('//*[@id="lzform"]/div[5]/div/div/input[2]/@value')[0]
                    data[selector.xpath('//*[@id="captcha_field"]/@name')[0]] = value
                print(data)     
            except:
               # print(response.text)
                self.logger.error('login response error', ressponse.status_code)
                exit()
            response =  self.session.post(selector.xpath('//*[@id="lzform"]/@action')[0], data=data)
            try:
                assert response.status_code == 200
                self.logger.info('login successfully')
            except:
                self.logger.error('login failed')
                exit()
        except:
            self.logger.error('login error!')
            exit()
            
    def _get_captcha(self, url):
        print(url)
        response = self.session.get(url)
        with open("captcha.gif", 'wb') as f:
            for i in response:
                f.write(i)
        with open("captcha.gif", 'rb') as f:
            Image.open(f).show()
        os.remove("captcha.gif")
        return input("Input the captcha.\n")
        
    def _fetch_page(self, request):
        try:
            response =  self.session.get(request['url'], params=request['params'], headers=request['headers'], timeout=10)
            try:
                self.logger.debug("claw: {}".format(response.url))
                assert response.status_code == 200
                return response.text, response.url
            except AssertionError:
                self.logger.warning('{} {}'.format(response.status_code, response.url))
                sefl.logger.error(response.text)
                exit()
        except:
            self.logger.warning('Timeout {} {}'.format(request['url'], request['params']))
    
    def _get_headers(self):
        headers = {
            'User-Agent': base.srandmember(self.redis, 'user.agent'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': base.srandmember(self.redis, 'referer')
        }
        return headers
        
    def _index_content(self, request):
        while True: # fault tolerance
            data = self._fetch_page(request)
            if data:
               content, raw_url = data
               break
            else:
                time.sleep(30)
                # some other ways
        headers = self._get_headers()
        request = {
            'url': None,
            'headers': headers
        }
        return content, request
        
    def _comments_content(self, request):
        while True: # fault tolerance
            data = self._fetch_page(request)
            if data:
               content, raw_url = data
               break
            else:
                self.logger.debug('sum:{}, current:{}'.format(self.max_comments, self.comments_num))
                if self.comments_num == self.max_comments:
                    return None, None
                time.sleep(30)
                # some other ways
        url = raw_url.split('?')[0]
        headers = self._get_headers()
        headers['Host'] = url.split('/')[2]
        request = {
            'url': url,
            'headers': headers,
            'params': None
        }
        return content, request
            
    def _filter_index(self, request):
        content, request = self._index_content(request)
        selector = etree.HTML(content)
        try:
            movie_info = {
                'name': base.strip(
                    selector.xpath('//*[@id="content"]/h1/span/text()')
                ),
                'director': base.strip(
                    base.split_pop(selector.xpath('//*[@id="info"]/span[1]')[0].xpath('string(.)'), char='/')
                ),
                'writer': base.strip(
                    base.split_pop(selector.xpath('//*[@id="info"]/span[2]')[0].xpath('string(.)'), char='/')
                ),
                'actor': base.strip(
                    base.split_pop(selector.xpath('//*[@id="info"]/span[3]')[0].xpath('string(.)'), char='/')
                ),
                'type': base.strip(
                    selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:genre")]/text()')
                ),
            # area and language ???
                'release_date': base.strip(
                    selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:initialReleaseDate")]/text()')
                ),
                'runtime': base.strip(
                    selector.xpath('//*[@id="info"]/span[starts-with(@property, "v:runtime")]/text()')
                ),
                'comments': list(),
            } # value is list
            self.max_comments = int(
                self._get_num(
                    selector.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')
                )[0])
            if movie_info:
                self.logger.debug(movie_info)
                comments_url = selector.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/@href')[0].split('?')[0]
                request['headers']['Host'] = comments_url.split('/')[2]
                request['url'] = comments_url
                return movie_info, request
            else:
                self.logger.warning('{} {} Movie information is empty'.format(request['url'], request['params']))
                return None
        except:
            self.logger.warning('{} {} Filter failed'.format(request['url'], request['params']))
            return None
    
    def _get_num(self, string):
        if not (isinstance(string, list)):
            return None
        pattern = re.compile(r'[\d]+')
        data = pattern.findall(string[0])
        return data
            
    def _filter_comments(self, request):
        commenters = list()
        content, request = self._comments_content(request)
        if (not content) and (not content):
            return
        selector = etree.HTML(content)
        try:
            items = selector.xpath('//*[@class="comment"]')
            for item in items:
                print( base.strip(
                       item.xpath('./h3/span[@class="comment-info"]/a/text()')
                    ),
                    self._get_num(
                        item.xpath('./h3/span[@class="comment-info"]/span[1]/@class')
                    ),
                    base.strip(
                        item.xpath('./p/text()')
                    ),
                    base.strip(
                        item.xpath('./h3/span[@class="comment-vote"]/span/text()')
                    ))
                commenters.append({
                    'name': base.strip(
                        item.xpath('./h3/span[@class="comment-info"]/a/text()')),
                    'rating': self._get_num(
                        item.xpath('./h3/span[@class="comment-info"]/span[1]/@class')
                    ),
                    'rating_time': base.strip(
                        item.xpath('./h3/span[@class="comment-info"]/span[2]/text()')
                    ),
                    'comment': base.strip(
                        item.xpath('./p/text()')
                    ),
                    'comment_vote': base.strip(
                        item.xpath('./h3/span[@class="comment-vote"]/span/text()')
                    )
                })
                self.comments_num += 1
                self.logger.debug('comment number: {}'.format(self.comments_num))
                time.sleep(0.5)
            if commenters:
                return commenters, request
            else:
                return None
        finally:
            pass
        #except:
        #    self.logger.error('Filter comments error!\n')

    def worker(self):
        request = base.blpop(self.redis, 'movie.request')
        data = self._filter_index(request)
        if data:
            time.sleep(2)
            info, request = data
            info['comments'] = list()
            num = 0
            while True:
                request['params'] = {
                    'start': repr(self.comments_num)
                }
                data = self._filter_comments(request)
                if data == None:
                    # deal info
                    break
                else:
                    info['comments'].extend(data[0])
                    request = data[1]
                    num += 20

    def run(self):
        self.logger.info('----------start----------')
        self.worker()
        self.logger.info('----------^end^----------')

if __name__ == '__main__':
    spider = Download()
    spider.run()
