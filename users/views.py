from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

def user_home(request):
    return HttpResponse(request.user)

def login_page(request):
    logout(request)
    context = {
        'title':"Login"
    }
    return render(request,"users/login.html",context)

def login_view(request):
    email = password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_obj = User.objects.get(email  = email)
            user = authenticate(username=user_obj.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
            else:
                messages.warning(request,"Username or  password invalid!")
        except User.DoesNotExist:
            messages.danger(request,"Email you entered doesn't exist!")
            return redirect('/login/')
        
    return render(request,'users/login.html')