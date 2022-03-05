from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import User, Post
from posts.tests.data_for_test import (
    AUTHOR,
    POST_TITLE,
    POST_TEXT,
)

INDEX_URL = '/'
INDEX_TEMPLATE = 'posts/index.html'

POST_DETAIL_TEMPLATE = 'posts/post_detail.html'
PROFILE_TEMPLATE = 'posts/profile.html'


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.post = Post.objects.create(
            title=POST_TITLE,
            text=POST_TEXT,
            author=cls.user,
        )
        cls.POST_DETAIL_URL = f'/post/{cls.post.id}/'
        cls.PROFILE_URL = f'/profile/{cls.user}/'

    def setUp(self):
        self.guest_client = Client()

    def test_index_status_page(self):
        """Доступность главной страницы"""
        response = self.guest_client.get(INDEX_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_status_page(self):
        """Доступность страницы с постом"""
        response = self.guest_client.get(self.POST_DETAIL_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_status_page(self):
        """Доступность страницы профиля автора"""
        response = self.guest_client.get(self.PROFILE_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_urls_uses_correct_template(self):
        """URL-адрес соотвествует шаблону страницы"""
        templates_url_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
