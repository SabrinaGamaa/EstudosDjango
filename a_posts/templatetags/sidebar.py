from django.template import Library
from django.db.models import Count
from a_posts.models import *

register = Library()


@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None, user=None):
    categories = Tag.objects.all()
    top_post = Post.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
    top_comments = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
    context = {
        'categories' : categories,
        'tag' : tag,
        'top_post' : top_post,
        'top_comments' : top_comments,
        'user' : user,
    }
    
    return context