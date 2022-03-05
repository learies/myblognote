from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User, Post
from posts.tests.data_for_test import (
    AUTHOR,
    POST_TITLE,
    POST_TEXT,
)

INDEX_URL = reverse('posts:index')
INDEX_TEMPLATE = 'posts/index.html'

POST_DETAIL = 'posts:post_detail'
POST_DETAIL_TEMPLATE = 'posts/post_detail.html'

PROFALE = 'posts:profile'
PROFILE_TEMPLATE = 'posts/profile.html'


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.post = Post.objects.create(
            title=POST_TITLE,
            text=POST_TEXT,
            author=cls.user,
        )
        cls.POST_DETAIL_URL = reverse(
            POST_DETAIL,
            kwargs={'post_id': cls.post.id},
        )
        cls.PROFILE_URL = reverse(
            PROFALE,
            kwargs={'username': cls.user},
        )

    def setUp(self):
        self.guest_client = Client()

    def test_pages_uses_correct_template(self):
        """URL-адрес соответствуюет шаблону страницы"""
        templates_pages_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
        }
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_post_appear_in_page_index(self):
        """Тест отображения поста на главной странице"""
        response = self.guest_client.get(INDEX_URL)
        self.assertContains(response, self.post)

    def test_post_detail_appear_in_page_index(self):
        """Тест отображения поста на главной странице"""
        response = self.guest_client.get(self.POST_DETAIL_URL)
        self.assertContains(response, self.post)

    def test_profile_page(self):
        """Страница профиля пользователя"""
        response = self.guest_client.get(self.PROFILE_URL)
        self.assertContains(response, self.post)
