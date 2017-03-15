'''
爬虫闯关第一关 http://www.heibanke.com/lesson/crawler_ex00/
提示技能: 模拟登陆、csrf-token
来自 http://www.zhihu.com/question/20899988 黑板客的回答

这里成功实现了模拟登陆，写一下思路：
    1.提交登陆表单，查看POST方法文件的消息头、Cookie、参数
        消息头中的请求头没啥有价值的内容，请求网址与登陆网址是一样的
        Cookie倒是引起了注意。清除Cookie，直接打开登陆界面，服务器响应了一个同样名称的Cookie
        表单参数里有这三个选项：
            "csrfmiddlewaretoken" / "username" / "password"
            "csrfmiddlewaretoken"怎么来的呢？查看登陆页面的HTML源码文件，发现<form>后有这么一行：
                <input type='hidden' name='csrfmiddlewaretoken' value='3TwYYML662nMWaafvVDWg8pp6RVCAS1d' />
    2.模拟登陆步骤：
        a.opener.open(auth_url),得到Cookie与csrfmiddlewaretoken
        b.构造请求体req，包含Cookie的headers、有csrfmiddlewaretoken/username/password的data
        b.opener.open(req)，得到Cookie
'''

from urllib import request
from urllib import parse
from urllib import error
from http import cookiejar
import re

class third:
    def __init__(self):
        self.username = "1234567"
        self.password = "1234567890"
        self.auth_url = "http://www.heibanke.com/accounts/login"
        self.url = "http://www.heibanke.com/lesson/crawler_ex02/"
        self.csrfmiddlewaretoken = ""

    def __get_cookies(self, req):
        cookies = cookiejar.CookieJar()
        handler = request.HTTPCookieProcessor(cookies)
        opener = request.build_opener(handler)
        try:
            with opener.open(req) as f:
                if f.code == 200:
                    pattern = re.compile(r"<input.*?type='hidden'.*?name='csrfmiddlewaretoken'.*?value='(.*?)'.*>")
                    try:
                        self.csrfmiddlewaretoken = pattern.search(f.read().decode("utf-8")).group(1)
                        print("Achieved cookies and csrfmiddlewaretoken sucessfully")
                    except:
                        print("Achieved cookies sucessfully")
                    return cookies
                else:
                    print("Lost cookies")
        except error.URLError as e:
                if hasattr(e, "reason"):
                    print ("We failed to reach a server. Please check your url and read the Reason")
                    print ("Reason: {}".format(e.reason))
                elif hasattr(e, "code"):
                    print("The server couldn't fulfill the request.")
                    print("Error code: {}".format(e.code))
                exit()

    def __request(self, url, cookies=None):
        form = {
            "csrfmiddlewaretoken": self.csrfmiddlewaretoken,
            "username": self.username,
            "password": self.password
        }
        data = parse.urlencode(form).encode("utf-8")
        headers = {}
        header_cookie = ""
        for cookie in cookies:
            header_cookie = "{} {}={};".format(header_cookie, cookie.name, cookie.value)
        headers["Cookie"] = header_cookie.strip(' ;')
        req = request.Request(url, data, headers=headers)
        return req

    def __auth_cookies(self, pre_auth_cookies):
        req = self.__request(self.auth_url, pre_auth_cookies)
        cookies = self.__get_cookies(req)
        return cookies

    def guess_passwd(self, auth_cookies):
        for i in range(31):
            self.password = i
            req = self.__request(self.url, auth_cookies)
            print("正在猜测密码为{}".format(self.password))
            try:
                with request.urlopen(req) as f:
                    body = f.read().decode("utf-8")
                    if not "您输入的密码错误" in body:
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

    def start(self):
        pre_auth_cookies = self.__get_cookies(self.auth_url)
        auth_cookies = self.__auth_cookies(pre_auth_cookies)
        self.guess_passwd(auth_cookies)

spider = third()
spider.start()
