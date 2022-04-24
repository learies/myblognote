from django.urls import path

from .views import (add_comment, group_posts, index, post_create, post_detail,
                    post_edit, profile)

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('profile/<str:username>/', profile, name='profile'),
    path('group/<slug:slug>/', group_posts, name='group_posts'),
    path('create/', post_create, name='post_create'),
    path('post/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
]
