# -*- conding:utf-8 -*-
# 该文件是编写 自定义模板标签 代码的。其实模板标签本质上就是一个 Python 函数

from django import template # 导入 django 的 template 模块
from ..models import Post, Category

register = template.Library() # 实例化一个 template.Library 类

# 一、最新文章模板标签
# 将函数 get_recent_posts 装饰为 register.simple_tag ，这样就可以在模版中使用语法 {% get_recent_posts %}调用这个函数了
@register.assignment_tag
def get_recent_posts(num=5):
    # 这个函数的作用是获取数据库中前 num 篇文章
    return Post.objects.all().order_by('-create_time')[:num]

# 二、归档模板标签
@register.assignment_tag
def archives():
    # datetimes 函数 会返回一个列表，列表中的元素为每一篇文章的创建时间，且是 Python 的 datetime 对象，精确到月份，降序排列
    return Post.objects.datetimes('create_time', 'month', order='DESC')

# 三、分类模板标签
@register.assignment_tag
def get_categories():
    #
    return Category.objects.all()