# -*- coding: utf-8 -*-
import re
import scrapy
import time
from lxml import etree
from homework2.items import Homework2Item
from scrapy.selector import Selector


def get_info(infos):
    """
    辅助函数，提取infos里面的有用信息
    :param infos:
    :return:
    """
    stack = []
    for i in infos:
        s = re.sub(r'\n              ', '', i)
        s = re.split(f'\n', s)
        if s[0] and s[0] != '  ':
            stack.append(s[0])
    return stack


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        time.sleep(2)
        item = Homework2Item()
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for i in range(10):

            movie_name = movies[i].xpath("./div/span/text()")[0].extract()
            movie_infos = movies[i].xpath("./div/text()").extract()
            infos = get_info(movie_infos)
            movie_type = infos[0]
            movie_time = infos[2]
            item['movie_info'] = {'movie_name': movie_name, 'movie_type': movie_type, 'movie_time': movie_time}
            yield item


