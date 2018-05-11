from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from posts.forms import PostForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from braces.views import SelectRelatedMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from posts import forms

from .models import Post


class AllPosts(ListView):
    model = Post
    paginate_by = 3
    template_name = 'posts/post_list.html'
    def get(self, request):
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        args = {
            'posts': posts, 'users': users
        }
        return render(request, self.template_name, args)
    

def detail(request, slug, pk):
    post = get_object_or_404(Post, slug=slug, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})


class UserPosts(ListView):
    model = Post
    template_name = "posts/user_timeline.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class SinglePost(DetailView):
    model = Post


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

def profile(request, username):
    user = get_object_or_404(User.objects, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'posts/profile.html', {'username':username,'posts': posts})





def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'home/profile.html', args)


class HomeView(TemplateView):
    template_name = 'posts/post_list.html'

    def get(self, request):
        posts = Post.objects.all().order_by('-created')
        users = User.objects.exclude(id=request.user.id)
        

        args = {
            'posts': posts, 'users': users
        }
        return render(request, self.template_name, args)

    