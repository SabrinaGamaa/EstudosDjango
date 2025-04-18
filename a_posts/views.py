from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from a_posts.forms import *
from .forms import *


def home_view(request, tag=None):
    # print("-=" * 20)
    # print('Request Method: ', request.method)
    # if request.method == 'POST':
    #     print('Bye bye')
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:
        posts = Post.objects.all()
        
    categories = Tag.objects.all()
    
    context = {
        'posts': posts,
        'categories' : categories,
        'tag' : tag
    }
        
    return render(request, 'a_posts/home.html', context)


def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        # Verifica se o formulário foi preenchido corretamente
        if form.is_valid():

            # Cria um objeto Post com os dados do formulário, mas ainda não salva no banco
            post = form.save(commit=False)

            # Faz a requisição para a URL digitada no formulário
            website = requests.get(form.data['url'])

            # Lê e interpreta o código HTML da página
            sourcecode = BeautifulSoup(website.text, 'html.parser')

            # Encontra a imagem da página (URL da imagem que começa com https://live.staticflickr.com/)
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image  # Salva a imagem no objeto post

            # Encontra o título da imagem no HTML (dentro da tag <h1 class="photo-title">)
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title  # Salva o título no objeto post

            # Encontra o nome do artista (dentro da tag <a class="owner-name">)
            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist  # Salva o artista no objeto post

            # Agora sim, salva tudo no banco de dados
            post.save()
            form.save_m2m()
            # Redireciona o usuário de volta para a página inicial
            return redirect('home')

    
    return render(request, 'a_posts/post_create.html', {'form' : form})
 
 
def post_delete_view(request, pk):
    referer = request.META.get('HTTP_REFERER', '/')
    post = get_object_or_404(Post, id=pk)
    
    if request.method == "POST":
        post.delete()
        
        messages.success(request, 'Post deleted')
        
        return redirect('home')
    
    return render (request, 'a_posts/post_delete.html', {'post' : post, 'referer' : referer})


def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, 'Post Updated')
            return redirect('home')
    
    context = {
        'post' : post,
        'form' : form
    }
    return render(request, 'a_posts/post_edit.html', context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'a_posts/post_page.html', {'post' : post})
