from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
# Create your views here.

def user_home(request):
    return HttpResponse(request.user)

def login_page(request):
    logout(request)
    return render(request,"users/login.html")
