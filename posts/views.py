from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http.response import HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {
        'posts': posts
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    total_likes = post.total_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    return render(request, 'post_detail.html', {
        'post': post,
        'total_likes': total_likes,
        'liked': liked
    })


def validate_fields_empty(request):
    if not request.POST['username'] or not request.POST['password1'] or not request.POST['password2']:
        return False
    return True


def is_match(request):
    return request.POST['password1'] == request.POST['password2']


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    if not validate_fields_empty(request):
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'You need to complete all the fields'

        })

    if is_match(request):
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

    return render(request, 'signup.html', {
        'form': UserCreationForm,
        'error': 'Password do not match'
    })


def validate_request(request):
    if not request.POST['username'] or not request.POST['password']:
        return False
    return True


def is_authenticate(request):
    return authenticate(request, username=request.POST['username'],
                        password=request.POST['password'])


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    if not validate_request(request):
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'You need to complete all the fields'
        })

    user = is_authenticate(request)
    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
        })

    login(request, user)
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('home')


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        return redirect('/post_detail/' + str(post_id))

    post.likes.add(request.user)
    return redirect('/post_detail/' + str(post_id))
