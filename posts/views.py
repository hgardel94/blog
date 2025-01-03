from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, RSSFeed
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http.response import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import feedparser
from django.utils.html import strip_tags
from django.utils.text import Truncator





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
        
    user = authenticate(request, username=request.POST['username'],
                        password=request.POST['password'])
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


@login_required(login_url='/')
def like_post(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)
        if request.user not in post.likes.all():
            post.likes.add(request.user)
            liked = True
        else:
            liked = False
        post.save()
        likes = post.likes.count()  
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
        likes = post.likes.count()  
        return JsonResponse({'liked': liked, 'likes': likes})
    return JsonResponse({'error': 'Invalid request method'}, status=400)



import html  

def update_posts_from_feed(request):
    # Obtener la URL del feed desde el parámetro GET
    feed_url = request.GET.get('feed_url', None)
    
    if not feed_url:
        return HttpResponse("No se proporcionó una URL de feed.", status=400)
    
    # Procesar el feed RSS
    feed = feedparser.parse(feed_url)
    
    if feed.bozo:
        return HttpResponse(f"Error al leer el feed: {feed.bozo_exception}", status=400)
    
    # Crear los posts a partir del feed
    for entry in feed.entries:
        # Verificar si ya existe un post con el mismo título
        post_exists = Post.objects.filter(title=entry.title).exists()
        
        # Si el post no existe, lo creamos
        if not post_exists:
            # Limpiar las etiquetas HTML en el título
            clean_title = strip_tags(entry.title)  # Limpiamos el título de las etiquetas HTML

            # Obtener el resumen (content o summary) y limpiarlo de etiquetas HTML
            full_summary = entry.summary  # Utilizamos el resumen si está disponible
            
            # Limpiar las etiquetas HTML en el resumen
            clean_summary = strip_tags(full_summary)  # Limpiamos las etiquetas HTML

            # Limpiar las entidades HTML (como &#39;, &nbsp;, etc.)
            clean_summary = html.unescape(clean_summary)  # Limpiamos las entidades HTML
            
            # Crear el post con el contenido limpio
            Post.objects.create(
                title=clean_title,  # Guardamos el título limpio
                content=clean_summary,  # Guardamos el resumen limpio
                created=entry.published,
            )
    
    return HttpResponse("Posts actualizados desde el feed.")
