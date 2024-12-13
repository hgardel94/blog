from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http.response import HttpResponse
from django.db import IntegrityError

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
        if not request.POST['username'] or not request.POST['password1'] or not request.POST['password2']:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'You need to complete all the fields'

            })

        elif request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })

        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    else:
        if not request.POST['username'] or not request.POST['password']:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'You need to complete all the fields'
            })
        else:
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Username or password is incorrect'
                })

            else:
                login(request, user)
                return redirect('home')


def signout(request):
    logout(request)
    return redirect('home')
