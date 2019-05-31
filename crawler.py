from requests_html import HTMLSession
import re
from .blog.models import (Article, Tag, Category)


class Spider:
    def __init__(self):
        self.sesion = HTMLSession()

    def get_list(self):
        url = 'http://python.jobbole.com/all-posts/'
        resp = self.sesion.get(url)
        if resp.status_code == 200:
            links = re.findall('(http://python.jobbole.com/\d+/)', resp.text)
            return set(links)
        return

    def get_detail(self, detail_url):
        resp = self.sesion.get(detail_url)
        if resp.status_code == 200:
            # text = resp.text
            return resp

    def parser(self, resp):
        #text = resp.html.find('.entry > p')
        text = ''.join(list(map(lambda x: x.text, resp.html.find('div.entry p'))))
        author = resp.html.find('div.entry div.copyright-area a', first=True).text
        temp = resp.html.find('p.entry-meta-hide-on-mobile', first=True).text.strip().split('·')
        createtime = temp[0]
        category = temp[1]
        tag = temp[-1]
        # print(createtime)
        # print(category)
        # print(tag)
        # print('================================================')
        Article.objects.create(created_time=createtime, )


if __name__ == '__main__':
    test = Spider()
    links = test.get_list()
    if links:
        for i in links:
            resp = test.get_detail(i)
            text = test.parser(resp)

