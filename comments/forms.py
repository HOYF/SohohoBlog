# -*- conding:utf-8 -*-

from django import forms
from .models import Comment

# Django的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类，如果表单对应有一个数据库模型，那么使用 ModelForm 类会简单很多
class CommentForm(forms.ModelForm):
    class Meta: #我们在表单内部类 Meta 里指定一些和表单相关的东西
        model = Comment # 表明这个表单对应的数据库模型是 Comment 类
        fields = ['name', 'email', 'url', 'text'] # 指定了表单需要显示的字段，这里我们指定了 name、email、url、text需要显示


