from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    group = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'group')
