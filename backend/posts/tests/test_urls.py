from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import User, Post, Group
from posts.tests.data_for_test import (
    AUTHOR,
    POST_TITLE,
    POST_TEXT,
    INDEX_TEMPLATE,
    POST_DETAIL_TEMPLATE,
    PROFILE_TEMPLATE,
    GROUP_TEMPLATE,
)

INDEX_URL = '/'


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
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.POST_DETAIL_URL = f'/post/{cls.post.id}/'
        cls.PROFILE_URL = f'/profile/{cls.user}/'
        cls.GROUP_URL = f'/group/{cls.group.slug}/'

    def setUp(self):
        self.guest_client = Client()

    def test_status_page(self):
        """Проверка статус код страницы"""
        client_url_status = {
            INDEX_URL: HTTPStatus.OK,
            self.POST_DETAIL_URL: HTTPStatus.OK,
            self.PROFILE_URL: HTTPStatus.OK,
            self.GROUP_URL: HTTPStatus.OK,
        }
        for client_url, status_code in client_url_status.items():
            with self.subTest(client_url=client_url):
                response = self.guest_client.get(client_url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template(self):
        """URL-адрес соотвествует шаблону страницы"""
        templates_url_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
            self.GROUP_URL: GROUP_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
