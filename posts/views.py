from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http.response import HttpResponse

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {
        'posts': posts
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post_detail.html', {
        'post': post
    })
    
def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
        'form': UserCreationForm
    })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'],
                password = request.POST['password1'])
                user.save()
                return HttpResponse('User create succesfully')
            
            except:
                return HttpResponse('Username already exist')
            
        else:
            HttpResponse('Password do not match')
            


def signin(request):
    return render(request, 'signin.html')
