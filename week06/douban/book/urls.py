"""
coding:utf8
@Time : 2020/8/30 21:23
@Author : cjr
@File : urls.py
"""

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book),
]
