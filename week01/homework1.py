"""
coding:utf8
@Time : 2020/7/21 22:35
@Author : cjr
@File : homework1.py
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def drop_space(s: str):
    """
    辅助函数
    只获取电影类型和时间
    :param s:
    :return:
    """
    return s.split(':')[1].strip()


def get_html() -> str:
    """
    获取URL响应页面
    :return:
    """
    url = 'https://maoyan.com/films?showType=3'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    # cookie不知道什么时候会失效
    cookie = 'uuid=A80EA400CA8E11EA9B0959085D74EA3D323803EEE85C403B893019E92A8A798E'

    header = {
        'User-Agent': user_agent,
        'CooKie': cookie,
    }
    response = requests.request('GET', url=url, headers=header)
    return response.text


def movie_spider(html: str):
    """
    爬取猫眼电影（https://maoyan.com/films?showType=3）前十个电影
    :param html:
    :return:
    """
    movie_list = []
    bs_info = bs(html, 'html.parser')
    attrs_div = bs_info.find_all('div', attrs={'class': 'movies-list'})
    tags = attrs_div[0].find_all('dl', attrs={'class': 'movie-list'})[0]

    movies_info = tags.find_all('div', attrs={'class': 'movie-hover-info'})

    for i in range(10):
        movie_name = movies_info[i].find_all('span', attrs={'class': 'name'})[0].text
        tmp = movies_info[i].find_all('div', attrs={'class': 'movie-hover-title'})
        movie_type = drop_space(tmp[1].text.strip())
        movie_time = drop_space(tmp[3].text.strip())
        movie_list.append([f'电影名称：{movie_name}', f'电影类型：{movie_type}',
                           f'上映时间：{movie_time}', '-------------------------'])
    return movie_list


def save_csv(movie_list):
    """
    使用pandas保存到csv文件
    :param movie_list:
    :return:
    """

    movies = pd.DataFrame(movie_list)

    movies.to_csv('movies1', sep='\n', encoding='utf8', index=False, header=False)


if __name__ == '__main__':
    movies_list = movie_spider(get_html())
    save_csv(movies_list)



