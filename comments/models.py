# -*- conding:utf-8 -*-
from django.db import models
from django.utils.six import python_2_unicode_compatible

#该装饰器用于兼容 python2
@python_2_unicode_compatible
class Comment(models.Model):
    # 评论用户的名字
    name = models.CharField(max_length=100)
    # 评论用户的邮箱
    email = models.EmailField(max_length=255)
    # 评论用户的个人网站
    url = models.URLField(blank=True)
    # 评论用户的发表的内容
    text = models.TextField()
    # 评论用户的发表评论的时间，auto_now_add=True意思是当评论数据保存到数据库时，自动把 create_tiem 的值指定为当前时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 该评论关联到哪一篇文章，因为一个评论只能属于一篇文章，而一篇文章可以有多个评论，是一对多的关系
    post = models.ForeignKey('hoBlog.Post')

    def __str__(self):
        return self.text[:20]

