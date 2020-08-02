"""
coding:utf8
@Time : 2020/8/1 18:26
@Author : cjr
@File : errors.py
自定义异常
"""


class GetIpFailRequest(BaseException):
    """
    http 请求错误
    """
    def __init__(self, details=None):
        super().__init__(self, details)
        self.status = 400
        self.details = details

    def __str__(self):
        return self.details


