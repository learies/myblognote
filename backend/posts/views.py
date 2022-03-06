from django.shortcuts import render
from django.shortcuts import get_object_or_404

from posts.models import Post, User, Group


def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'posts/profile.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.all()
    context = {
        'posts': posts,
        'group': group,
    }
    return render(request, 'posts/group_posts.html', context)
