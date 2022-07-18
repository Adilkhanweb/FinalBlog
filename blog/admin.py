from django.contrib import admin
from .models import *


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_thumbnail')


admin.site.register(Post, PostAdmin)
admin.site.register(PostView)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Category)
