from django.contrib import admin
from .models import Category,Post,Comment,Tag


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
