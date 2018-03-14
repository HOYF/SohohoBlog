# -*- conding:utf-8 -*-
# 该文件是编写 自定义模板标签 代码的。其实模板标签本质上就是一个 Python 函数

from django import template # 导入 django 的 template 模块
from ..models import Post, Category
from django.db.models.aggregates import Count

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
    # return Category.objects.all()

    # Count 计算分类下的文章数，其接受的参数为需要计算的模型名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
# 这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，它会返回数据库中全部 Category 的记录，
# 但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
# 代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
# 然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，
# 最后把这个值保存到 num_posts 属性中。

# 此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。
# 因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示
