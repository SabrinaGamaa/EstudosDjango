from django.db import models
from django.contrib.auth.models import User
import uuid

class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    url = models.URLField(max_length=500, null=True)
    image = models.URLField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    body = models.TextField()
    likes =models.ManyToManyField(User, related_name="likedposts", through="LikedPost")
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)


    class Meta:
        ordering = ['-created']


class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'
        
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        
        

class Comment(models.Model):
    # Referência ao autor do comentário; mantém o comentário mesmo se o usuário for deletado
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    # Referência ao post ao qual o comentário pertence; exclui comentários se o post for deletado
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Conteúdo do comentário (limite de 150 caracteres)
    body = models.CharField(max_length=150)
    
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment' )
    
    # Data de criação do comentário
    created = models.DateTimeField(auto_now_add=True)
    # ID único do comentário, gerado automaticamente com UUID
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'
          
    class Meta:
        ordering = ['-created']
        
        
class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'
 

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedreplys', through='LikedReply' )
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'
        
     
    class Meta:
        ordering = ['-created']
        
        
class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'