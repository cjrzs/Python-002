"""
coding:utf8
@Time : 2020/8/1 21:49
@Author : cjr
@File : mysql_utils.py
"""
import pymysql


def connect_mysql(query):
    """
    链接数据库
    :param query: sql语句
    :return:
    """
    con = pymysql.connect(
        host='47.105.70.179',
        user='root',
        password='***',
        database='maoyan',
        port=3306,
        charset='utf8')
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    rawvalues = cur.fetchall()
    cur.close()
    con.close()
    return rawvalues


def mysql_insert_maoyan_movies(movie_name, movie_type, movie_time):
    """
    插入语句（针对smartDR）
    :param server:
    :param command:
    :param email:
    :return:
    """
    query = f'insert into movies (movie_name, movie_type, movie_time) ' \
        f'values ("{movie_name}", "{movie_type}", "{movie_time}");'

    result = connect_mysql(query=query)
    return result