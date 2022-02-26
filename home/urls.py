from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_view,name='home'),
    path('blogs/',views.blog_all,name='blog'),
    path('blog/<slug:slug>/', views.blog_details, name='blog_det'),
    path('createblog/', views.AddBlogView.as_view(), name='blog_create'),
    path('createblog/done', views.AddBlogView.as_view(), name='blog_created'),
    path('<slug>/update/', views.update_view, name='update_vi' ),
    path('<slug>/delete/', views.blog_delete_view, name='delete' ),
    path('blogs/<username>/', views.user_blog, name='user-blogs' ),
    path('blogs/create/new/',views.create_blog,name="create-blog-one")
]