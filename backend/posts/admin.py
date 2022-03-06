from django.contrib import admin

from posts.models import Post, Group


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
