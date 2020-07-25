# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd


class Homework2Pipeline(object):
    def process_item(self, item, spider):
        movies_info = item['movie_info']
        movie_name = movies_info['movie_name']
        movie_type = movies_info['movie_type']
        movie_time = movies_info['movie_time']
        output = f'电影名称：{movie_name}\n电影类型：{movie_type}\n上映时间：{movie_time}\n----------------------\n'

        with open('maoyanmovie.csv', 'a+', encoding='utf8') as f:
            f.write(output)
        return item


