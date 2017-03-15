#/usr/bin/env python
'''
黑板客爬虫闯关第四关
http://www.heibanke.com/lesson/crawler_ex03/
使用协程
python 3.5
aiohttp 0.21.2
'''

import asyncio
import aiohttp
import requests
from lxml import etree
from itertools import count

class Four:
    def __init__(self, *, username, password):
        self.payload = {'username': username, 'password': password}
        self.cookies = None
        self.password = dict()
  
    def _login(self):
        login_url = 'http://www.heibanke.com/lesson/crawler_ex03/'
        with requests.Session() as session:
            req = session.get(login_url)
            if req.status_code is 200:
                self.payload['csrfmiddlewaretoken'] = session.cookies['csrftoken']
                response = session.post(req.url, data=self.payload)
                try:
                    assert response.status_code == 200
                    self.cookies = dict(session.cookies)
                    print("login")
                except AssertionError:
                    print('login failed, try again')
                    exit()
            else:
                print('login url error')
                
    async def fetch_page(self, session, url):
        async with session.get(url, compress=True) as response:
            try:
                assert response.status == 200
                print(response.url, 'sucessfully')
                return await response.text()
            except AssertionError:
                print(url, response.status , "error!")
    
    async def filter_page(self, session, url):
        page = await self.fetch_page(session, url)
        if page:
            selector = etree.HTML(page)
            data = selector.xpath('//td/text()')        
            for i in range(int(len(data)/2)):
                self.password[data[2*i]] = data[2*i+1]
            print(self.password)
    
    def main(self):
        url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/?page='
        self._login()
        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop, cookies=self.cookies) as session:
            for i in count(0, 2):
                loop.run_until_complete(asyncio.wait([self.filter_page(session, url+repr(i%14+1)) for i in range(i, i+2)]))
                if len(self.password) is 100:
                    break
                    
    def passwd(self):
        password = ''
        print(self.password)
        for i in range(1, 101):
            password += self.password[repr(i)]
        print('password is {}'.format(password))
        
if __name__ == '__main__':
    print('------------------------start-----------------------')
    spider = Four(username='feather12315', password='w12315')
    spider.main()
    spider.passwd()
    print('-------------------------end------------------------')