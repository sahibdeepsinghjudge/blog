from django.urls import path
from . import views
urlpatterns = [
    path('',views.user_home,name='user-home'),
    path('authenticate/',views.login_view,name='login-auth-view'),
]