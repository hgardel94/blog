from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http.response import JsonResponse
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.




def home(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page = request.GET.get("page") or 1
    posts = paginator.get_page(page)
    current_page = int(page)
    pages = range(1, posts.paginator.num_pages + 1)
    for post in posts:
        if request.user in post.likes.all():
            post.likes_minus_one = post.likes.count() - 1
        else:
            post.likes_minus_one = post.likes.count()
    return render(request, 'home.html', {
        'posts': posts,
        'pages': pages,
        'current_page': current_page,
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


def validate_empty_fields(request):
    if not request.POST['username'] or not request.POST['password1'] or not request.POST['password2']:
        return False
    return True


def password_match_validator(request):
    return request.POST['password1'] == request.POST['password2']


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    if not validate_empty_fields(request):
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'You need to complete all the fields'

        })

    if password_match_validator(request):
        try:
            user = User.objects.create_user(username=request.POST['username'],
                                            password=request.POST['password1'])
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



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required(login_url='/')
def give_like_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            liked = True
        else:
            liked = False
        post.save()
        likes = post.likes.count()  # Asegúrate de actualizar el conteo de likes
        return JsonResponse({'liked': liked, 'likes': likes})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/')
def remove_like_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            liked = True
        post.save()
        likes = post.likes.count()  # Asegúrate de actualizar el conteo de likes
        return JsonResponse({'liked': liked, 'likes': likes})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


