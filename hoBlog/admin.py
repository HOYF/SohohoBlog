from django.contrib import admin
from .models import Post, Category, Tag
# Register your models here.

# 为了显示更详细的内容
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)


