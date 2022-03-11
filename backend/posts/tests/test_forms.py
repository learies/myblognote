from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User, Post, Group
from posts.forms import PostForm
from posts.tests.data_for_test import (
    AUTHOR,
    POST_TITLE,
    POST_TEXT,
    GROUP_TITLE,
    GROUP_SLUG,
    DESCRIPTION,
)

CREATE_POST = 'posts:post_create'
PROFALE = 'posts:profile'

POST_TITLE_TWO = 'Второй тестовый заголовок'
POST_TEXT_TWO = 'Второй тестовый текст поста'


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=GROUP_TITLE,
            slug=GROUP_SLUG,
            description=DESCRIPTION,
        )
        cls.post = Post.objects.create(
            title=POST_TITLE,
            text=POST_TEXT,
            author=cls.user,
        )
        cls.CREATE_POST_URL = reverse(
            CREATE_POST,
        )
        cls.PROFILE_URL = reverse(
            PROFALE,
            kwargs={'username': cls.user},
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post"""
        posts_count = Post.objects.count()
        form_data = {
            'title': POST_TITLE_TWO,
            'text': POST_TEXT_TWO,
            'slug': GROUP_SLUG,
        }
        response = self.authorized_client.post(
            self.CREATE_POST_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, self.PROFILE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                title=POST_TITLE_TWO,
                text=POST_TEXT_TWO,
            ).exists()
        )
