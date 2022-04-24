from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def _get_post_detail(post_id: int) -> Post:
    """Возвращает пост по id или 404 если нет такого поста."""
    return get_object_or_404(Post, pk=post_id)


def index(request) -> render:
    """Выводит шаблон страницы со списком всех постов."""
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def post_detail(request, post_id) -> render:
    """Выводит шаблон страницы с одним постом."""
    post = _get_post_detail(post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username) -> render:
    """Выводит шаблон страницы со списоком постов автора."""
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'posts/profile.html', context)


def group_posts(request, slug) -> render:
    """Выводит шаблон страницы со списоком постов группы."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.all()
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_posts.html', context)


@login_required
def post_create(request) -> render or redirect:
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    context = {
        'form': form,
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id) -> render or redirect:
    post = _get_post_detail(post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post.id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None,
            instance=post
        )
        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id=post.id)
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
