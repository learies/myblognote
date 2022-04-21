from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer, StringRelatedField

from posts.models import Post

class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'pub_date', 'author', 'group')
