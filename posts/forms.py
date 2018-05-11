from django import forms
from .models import Post
from django.contrib.admin import widgets

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'draft', 'publish', 'slug']

class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())


class HomeForm(forms.ModelForm):
    post = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write a post...'
        }
    ))

    class Meta:
        model = Post
        fields = ('title',)
