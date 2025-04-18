from django.forms import ModelForm
from django import forms
from a_posts.models import Post

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body' : 'Caption',
            'tags' : 'Category',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows' : 3, 'placeholder' : 'Add a capition ...', 'class' : 'font1 text-4xl'}),
            'url' : forms.TextInput(attrs={'placeholder' : 'Add url ...'}),
            'tags' : forms.CheckboxSelectMultiple(),
        }
        

class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'tags']
        labels = {
            'body' : 'Edit',
            'tags' : 'Category',
        }
        widgets = {
            'body' : forms.Textarea(attrs={'rows' : 3, 'placeholder' : 'Add a capition ...', 'class' : 'font1 text-4xl'}),
            'tags' : forms.CheckboxSelectMultiple(),
        }