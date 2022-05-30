from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Group, Post, User


def _get_post_detail(post_id: int) -> Post:
    """Возвращает пост по id или 404."""
    return get_object_or_404(Post, pk=post_id)


def index(request) -> render:
    """Выводит список всех постов."""
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def post_detail(request, post_id) -> render:
    """Выводит пост по post_id."""
    post = _get_post_detail(post_id)
    form = CommentForm(request.POST or None)
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


def profile(request, username) -> render:
    """Выводит список постов автора."""
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'posts/profile.html', context)


def group_posts(request, slug) -> render:
    """Выводит список постов группы."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.all()
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_posts.html', context)


@login_required
def post_create(request) -> render or redirect:
    """Создать пост."""
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
    """Редактирование поста."""
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


@login_required
def add_comment(request, post_id):
    """Добавляет комментарии к посту."""
    post = _get_post_detail(post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)
