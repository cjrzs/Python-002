# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .utils import mysql_utils


class Homework2Pipeline(object):
    def process_item(self, item, spider):
        movies_info = item['movie_info']
        movie_name = movies_info['movie_name']
        movie_type = movies_info['movie_type']
        movie_time = movies_info['movie_time']
        try:
            mysql_utils.mysql_insert_maoyan_movies(movie_name, movie_type, movie_time)
        except Exception as e:
            print(f'mysql写库失败\n{e}')
        return item


