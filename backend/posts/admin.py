from django.contrib import admin

from .models import Comment, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'pub_date',
        'author',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
        'pub_date',
    )
