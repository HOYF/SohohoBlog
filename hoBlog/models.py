# -*- conding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.utils.six import python_2_unicode_compatible



# 分类数据库表
# python_2_unicode_compatible 装饰器用于兼容 python2
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 标签数据库表
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 文章数据库表
@python_2_unicode_compatible
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文，存储比较短的字符串可以使用CharField，但对于文章但正文来说可能会是一大段文字，因此使用TextField来存储打断文本
    body = models.TextField()
    # 创建时间
    create_time = models.DateTimeField()
    # 最后修改时间
    modified_time = models.DateTimeField()
    # 文章摘要，可以没有文章摘要，但默认情况下CharField要求我们必须存入数据，否则会报错，
    # 指定CharField的blank=True 参数值后就可以允许空值了
    excerpt = models.CharField(max_length=200, blank=True)
    # 关联文章分类数据表，我们规定一篇文章只能对应一个分类，但是一个分类下可能有多篇文章
    # 所以我们使用ForeignKey，即一对多的关联关系
    category = models.ForeignKey(Category)
    # 关联文章标签数据表，我们规定一篇文章可以有多个标签，同一个标签下也可能有多篇文章
    # 所以我们使用ManyToManyField，表明是多对多的关联关系，同时我们规定文章可以没有标签，所以blank=True
    tags = models.ManyToManyField(Tag, blank=True)
    # 文章作者，这里User是从 django.contrib.auth.models 导入的
    # django.contrib.auth.models 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，
    # User 是 Django 为我们写好的用户模型，这里我们通过ForeignKey 把文章和 User关联起来
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会有多篇文章，因此这是一个一对多的关联关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    # 注意到 URL 配置中的 url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail') ，我们设定的 name='detail' 在这里派上了用场。
    # 看到这个 reverse 函数，它的第一个参数的值是 'hoBlog:detail'，意思是 hoBlog 应用下的 name=detail 的函数，
    # 由于我们在urls.py 添加了该代码 namespace='hoBlog'， 告诉了 Django 这个 URL 模块是属于 hoBlog 应用的，
    # 因此 Django 能够顺利地找到 hoBlog 应用下 name 为 detail 的视图函数，于是 reverse 函数会去解析这个视图函数对应的 URL，
    # 我们这里 detail 对应的规则就是 post/(?P<pk>[0-9]+)/ 这个正则表达式，而正则表达式部分会被后面传入的参数 pk 替换，
    # 所以，如果 Post 的 id（或者 pk，这里 pk 和 id 是等价的） 是 255 的话，那么 get_absolute_url 函数返回的就是 /post/255/ ，
    # 这样 Post 自己就生成了自己的 URL。
    def get_absolute_url(self):
        return reverse('hoBlog:detail', kwargs={'pk': self.pk})

    # 为了让文章Post 按发布时间逆序排列，哥哥视图函数中都有类似于 Post.objects.all().order_by('-create_time) 这样的代码，这导致了很多重复
    # 因为只要是返回的文章列表，基本都是逆序排列的，因此我们可以在 Post 模型中指定 Post 的自然排序方式
    # Django允许我们在 models.Model 的子类里定义一个 Meta 的内部类，这个内部类通过指定一些属性来规定这个类该有的一些特性，
    # 例如在这里我们要指定 Post 的排序方式
    class Meta:
        # ordering 属性用来指定文章排序方式， ['-create_time'] 指定了依据哪个属性的值进行排序，这里指定为按照文章发布时间排序，且负号表示逆序排列
        # 列表中可以用多个项，比如 ordering = ['-create_time', 'title]，那么首先依据 create_tiem 排序，如果 create_tiem 相同，则在依据 title 排序
        # 这样指定以后所有的返回的文章列表都会自动按照 Meta 中指定的顺序排序，因此可以删掉视图函数中对文章列表中返回结果进行排序的代码来
        ordering = ['-create_time']
