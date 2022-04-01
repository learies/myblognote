from django.urls import path

from posts.views import (
    index,
    post_detail,
    profile,
    group_posts,
    post_create,
    post_edit,
)

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('profile/<str:username>/', profile, name='profile'),
    path('group/<slug:slug>/', group_posts, name='group_posts'),
    path('create/', post_create, name='post_create'),
    path('post/<post_id>/edit/', post_edit, name='post_edit'),
]
