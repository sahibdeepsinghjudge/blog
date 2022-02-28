from dataclasses import fields
from importlib.metadata import files
from pyexpat import model
from django.contrib import admin

from .models import blog_Details,blog, tags

# Register your models here.


class blogAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'blog_clicks', 'date')
    search_fields = ("blog_title__startswith", )
    prepopulated_fields = {'slug': ('blog_title','date')}
    orderring = 'blog_clicks'
admin.site.register(blog)
admin.site.register(blog_Details,blogAdmin)
admin.site.register(tags)
