import requests
from lxml import etree

def crawl(url):
    response = requests.get(url)
    try:
        assert response.status_code == 200
        return response.text
    except:
        print('error')

def parse(page):
    selector = etree.HTML(page)
    movie_urls = selector.xpath('//td[@valign="top"]/div/a/@href')
    print(len(movie_urls))

def main():
    for i in range(1988, 2016):
        page = crawl('https://movie.douban.com/tag/{}/?focus=movie'.format(repr(i)))
        parse(page)

if __name__ == '__main__':
    main()
