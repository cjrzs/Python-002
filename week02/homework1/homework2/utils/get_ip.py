"""
coding:utf8
@Time : 2020/8/1 17:21
@Author : cjr
@File : get_ip.py
"""
from . import errors
import requests


def get_ips():
    """
    github上的免费IP池：https://github.com/jiangxianli/ProxyIpLib.git
    响应消息格式：
    {
        "code":0,
        "msg":"成功",
        "data":{
            "current_page":1,
            "data":[
                {
                    "unique_id":"dd2aa4a97ab900ad5c7b679e445d9cde",
                    "ip":"119.167.153.50",
                    "port":"8118",
                    "ip_address":"山东省 青岛市",
                    "anonymity":0,
                    "protocol":"http",
                    "isp":"联通",
                    "speed":46,
                    "validated_at":"2017-12-25 15:11:05",
                    "created_at":"2017-12-25 15:11:05",
                    "updated_at":"2017-12-25 15:11:05"
                },
                {
                    "unique_id":"7468e4ee73bf2be35b36221231ab02d5",
                    "ip":"119.5.0.42",
                    "port":"22",
                    "ip_address":"四川省 南充市",
                    "anonymity":0,
                    "protocol":"http",
                    "isp":"联通",
                    "speed":127,
                    "validated_at":"2017-12-25 15:10:04",
                    "created_at":"2017-12-25 14:38:14",
                    "updated_at":"2017-12-25 15:10:04"
                }
            ],
            "last_page":1,
            "per_page":15,
            "to":8,
            "total":8
        }
    }
    :return:
    """
    res = []
    try:
        ips_info = requests.request('GET', 'https://ip.jiangxianli.com/api/proxy_ips').json()
    except Exception as e:
        print(e)
    ip_list = ips_info['data']['data']

    if not ip_list:
        raise errors.GetIpFailRequest('IP列表获取失败')
    for ip_info in ip_list:
        ip = ip_info['ip']
        protocol = ip_info['protocol']
        port = ip_info['port']
        res.append(f'{protocol}://{ip}:{port}')
    return res

