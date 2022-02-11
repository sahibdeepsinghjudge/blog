from django.contrib import admin

from .models import blog_Details,blog

# Register your models here.
admin.site.register(blog)
admin.site.register(blog_Details)
