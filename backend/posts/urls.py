from django.urls import path

from posts.views import index, post_detail

app_name = 'posts'

urlpatterns = [
    path('', index, name='index'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]
