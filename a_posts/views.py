from django.shortcuts import render, redirect
from django.forms import ModelForm
from django import forms
from a_posts.models import Post
from bs4 import BeautifulSoup
import requests

def home_view(request):
    print("-=" * 20)
    print('Request Method: ', request.method)
    if request.method == 'POST':
        print('Bye bye')
        
    posts = Post.objects.all()
    return render(request, 'a_posts/home.html', {'posts': posts})


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body']
        labels = {
            'body' : 'Caption',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows' : 3, 'placeholder' : 'Add a capition ...', 'class' : 'font1 text-4xl'}),
            'url' : forms.TextInput(attrs={'placeholder' : 'Add url ...'})
        }


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

            # Redireciona o usuário de volta para a página inicial
            return redirect('home')

    
    return render(request, 'a_posts/post_create.html', {'form' : form})
 