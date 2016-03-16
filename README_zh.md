# wander

使用 aiohttp 的简易爬虫框架。

## 语言

[EN](README.md)  [ZH](README_zh.md)

## 介绍

不满于 [scrapy](https://github.com/scrapy/scrapy) 这种笨重的框架； 感觉 [pyspider](https://github.com/binux/pyspider) 的依赖有点多。最重要的是，他们都不支持最新版本的 Python！自己又偏向简洁，加之深究下爬虫，遂写了这个玩具。

三个模块

* claw.py -- 抓取
* filter.py -- 过滤
* proxy -- 代理验证

## 特点

* 使用原生异步库`asyncio` -- ！！限于水平，目前仅仅实现了 Linux 下正常工作
* 极少的依赖 -- 仅仅需要`aiohttp` / `redis` / `pymongo`
* 自定义HTML解析库 -- 使用您想要的HTML解析库定义提取规则
* 支持 HTTP - 非 HTTPS - 代理
* 协程爬取 / 多进程过滤
* Redis 充当缓存队列
* 数据持久化至 MongoDB 中 -- 未完成

## LICENSE

[MIT license](LICENSE)

## 后记

断断续续捣鼓爬虫三月有余，从 urllib 至 requests，再到现在的 aiohttp。  

我所知到的

在速度方面，还欠缺 Bloom Filter 与集群化爬取。曾想过实现集群，却没有相应的资源，即使实现也属鸡肋，遂罢。而 Bloom Filter 现在也用不到，不予考虑。

不同于速度的发展方向 -- Ajax 异步加载 / 模拟登录 / 反反爬虫 / 验证码识别 / 解析 JavaScrpit 等等，应对策略只有基本常识 -- 提取 Ajax 地址 / session / 代理，后两个还没有做。

到现在这程度，也能满足一般的需求了。现在，还差一个守护进程~

timeline -- 2016/03/16