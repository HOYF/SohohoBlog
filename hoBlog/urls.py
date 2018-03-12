# -*- conding:utf-8 -*-

from django.conf.urls import url #导入url函数
from . import views #从当前目录下导入views模块

# 把网址和处理函数的关系写在 urlpatterns 列表里
# url()函数 【参数1：网址】【参数2：处理函数】【参数3：这个参数的值作为处理函数index的别名】
# 【^post/(?P<pk>[0-9]+)/$】表示以post/开头，后跟一个至少一位数的数字，并以/富豪结尾，其中 [0-9]+ 表示一位或多位数
# 此外，(?P<pk>[0-9]+) 叫命名捕获组，其作用是从用户访问的 URL 里把括号内匹配的字符串捕获并作为关键字传给其对应的试图函数 detail
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    # 两个括号括起来的地方是两个命名组参数，Django 会从用户访问的URL中自动提取这两个参数，然后传递给其视图函数，
    # 例如如果用户想查看2017年3月下的全部文章，他访问 /archives/2017/3，那么 archives 视图函数的时间调用为 archives(request,year=207,month=3)
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]
