from django.core.checks import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import blog, blog_Details
from django.contrib import messages
from django.views.generic.list import ListView
from .forms import blogForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from random import randint
def blog_all(request):
    blogs=blog_Details.objects.all().order_by('-id')[0:11]
    bloga=blog_Details.objects.all().order_by('-id')[0:1]
    
    context={
         'title':'Blog',
         'bloga':blogs,
         'blog':bloga,
        
    }
    return render(request,'blog/blog.html',context)

def blog_details(request,slug):
    blogd=blog_Details.objects.filter(slug=slug)
    
    if blogd:
        blog_object=blog_Details.objects.get(slug=slug)
        blogs=blog_Details.objects.all().order_by('-blog_clicks')[0:6]
        blog_content = blog.objects.get(blog_id = blog_object.id)
        blog_object.blog_clicks=blog_object.blog_clicks+1
        blog_object.save()
        if blog_object in blogs:
            trending = True
        else:
            trending = False
        context = {
            'title':'Blog | '+ blog_object.blog_title,
            'blog':blogd,
            'blog_content':blog_content.blog_content,
            'is_trending':trending,
        }
        return render(request,'blog/blog.html',context)
    else:
        messages.info(request,"Requested blog not found!")
        return redirect('/')

def create_blog_page(request):
    context = {
        'title':'Create Blog',
    }
    return render(request,'blog/createblog.html',context)
def create_blog(request):
    if request.method=='POST':
        blog_title = request.POST.get('title')
        brief = request.POST.get('brief')
        bloga = blog.objects.create(blog_title=blog_title,blog_brief=brief)
        bloga.save()
        messages.success(request,'Blog created')
    return redirect('/create-blog/write/')

class AddBlogView(ListView,LoginRequiredMixin):
    model = blog
    def get(self, request):
        if request.user.is_superuser:
            form = blogForm()
            return render(request, 'blog/createblog.html', {'form':form,'name':'Create Blog'})
        else:
            messages.info(request,'Access denied or 404')
        return redirect('/blog/')
   
    def post(self, request):
        form = blogForm(request.POST)
        if form.is_valid():
    
            blog_content = form.cleaned_data['blog_content']
            add_post = blog.objects.create( blog_content= blog_content)
            add_post.save()
            form = blogForm()
            messages.success(request,'Blog created')
            return redirect('/dashboard/')
        else:
            messages.error(request,"Process failed due to internal server error.")
            return redirect('/')
@login_required
def update_view(request, slug):
    # dictionary for initial data with 
    # field names as keys
    context ={}
  
    # fetch the object related to passed id
    blog_det = blog_Details.objects.get(slug=slug)
    obj = blog.objects.get(blog_id = blog_det.id)
    # pass the object as instance in form
    form = blogForm(request.POST or None, instance = obj)
  
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        messages.success(request,'Blog post updated')
        return redirect("/"+slug+'/')
       
    # add form dictionary to context
    context["form"] = form
    context["name"] = 'Update | '+blog_det.blog_title
     
    return render(request, "blog/createblog.html", context)
@login_required
def blog_delete_view(request,slug):
    if request.user.is_superuser:
        blog_det_obj = blog_Details.objects.get(slug=slug)
        blog_cont = blog.objects.get(blog_id = blog_det_obj.id)
        blog_det_obj.delete()
        blog_cont.delete()
        messages.success(request,"Your blog has been deleted!")
        return redirect('/')
    else:
        messages.error(request,"Action not completed")
        return redirect('/blog/',slug)

#home page

def home_view(request):
    blogs=blog_Details.objects.all().order_by('-blog_clicks')[0:6]
    blog_top=blog_Details.objects.all().order_by('-blog_clicks')[0:1]

    context={
         'title':'Blog',
         'blogs':blogs,
         'blog_top':blog_top,
        
    }
    
    return render(request,'home/index.html',context)

def user_blog(request,username):
    try:
        user_obj = User.objects.get(username=username)
        blogs = blog_Details.objects.filter(blog_creator = user_obj.id).order_by('-blog_clicks')
        blogs_list = []
        for i in blogs:
            blogs_list.append({'title':i.blog_title,'tags':i.tags,'date':i.date,'clicks':i.blog_clicks,'slug':i.slug})
        data = {
            'blogs':blogs_list,
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return redirect('/')

@login_required
def create_blog(request):
    return render(request,"blog/createblog_first.html")