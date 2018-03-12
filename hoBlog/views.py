# -*- conding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
import markdown
from comments.forms import CommentForm


def index(request):
    # 从数据库中获取全部文章，然后通过order_by()方法，按发表时间倒序
    # post_list = Post.objects.all().order_by('-create_time')
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={
        'post_list':post_list
    })

    # render() 【参数1：传入HTTP请求】【参数2：传入模版路径】【参数3 context：把模版中的变了替换为我们传递的变量值 】
    # return render(request, 'blog/index.html', context={
    #     'title':'我的博客首页',
    #     'welcome':'欢迎访问我的博客首页'
    # })

    # return HttpResponse("欢迎访问我的博客首页！")


def detail(request, pk):
    # 当 pk 存在时（在数据库中能找到）就放回对应的Post，如果不存在，就返回一个 404 错误，表明用户请求的文章不存在
    post = get_object_or_404(Post, pk=pk)
    # 将 Markdown 格式的文本渲染成HTML文本再传递给模板
    # extensions 是对 Markdown 语法的扩展，这里我们使用了三个拓展，分别是 extra、codehilite、toc。
    # extra 本身包含很多拓展
    # codehilite 是语法高亮的拓展
    # toc 是允许我们自动生成目录
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {'post':post,
               'form':form,
               'comment_list':comment_list
               }
    return render(request, 'blog/detail.html', context=context)


# 归档视图
def archives(request, year, month):
    # 使用 filter 函数来过滤文章
    # create_time是一个dateTime对象
    # post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month)
    return render(request, 'blog/index.html',context={'post_list':post_list})

# 分类视图函数
def category(request, pk):
    # 这里我们首先根据传入的pk值(也就是被访问的分类的id值)从数据库中获取到这个分类
    cate = get_object_or_404(Category, pk=pk)
    # 然后通过 filter 函数过滤出了该分类下的全部文章，并且根据时间倒序排列
    # post_list = Post.objects.filter(category=cate).order_by('-create_time')
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})