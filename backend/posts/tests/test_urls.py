from http import HTTPStatus

from django.test import Client, TestCase
from posts.models import Group, Post, User
from posts.tests.data_for_test import (AUTHOR, CREATE_POST_TEMPLATE,
                                       DESCRIPTION, GROUP_SLUG, GROUP_TEMPLATE,
                                       GROUP_TITLE, INDEX_TEMPLATE,
                                       POST_DETAIL_TEMPLATE, POST_TEXT,
                                       POST_TITLE, PROFILE_TEMPLATE)

INDEX_URL = '/'
CREATE_POST_URL = '/create/'
UNEXISTING_URL = '/unexisting_page/'


class StaticURLTests(TestCase):
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
        cls.POST_DETAIL_URL = f'/post/{cls.post.id}/'
        cls.PROFILE_URL = f'/profile/{cls.user}/'
        cls.GROUP_URL = f'/group/{cls.group.slug}/'
        cls.POST_EDIT_URL = f'/post/{cls.post.id}/edit/'

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_status_page_for_guest_client(self):
        """Проверка статус код страницы для не авторизованного пользователя"""
        client_url_status = {
            INDEX_URL: HTTPStatus.OK,
            self.POST_DETAIL_URL: HTTPStatus.OK,
            self.PROFILE_URL: HTTPStatus.OK,
            self.GROUP_URL: HTTPStatus.OK,
            CREATE_POST_URL: HTTPStatus.FOUND,
            self.POST_EDIT_URL: HTTPStatus.FOUND,
            UNEXISTING_URL: HTTPStatus.NOT_FOUND,
        }
        for client_url, status_code in client_url_status.items():
            with self.subTest(client_url=client_url):
                response = self.guest_client.get(client_url)
                self.assertEqual(response.status_code, status_code)

    def test_status_page_for_authorized_client(self):
        """Проверка статус код страницы для авторизованного пользователя"""
        client_url_status = {
            INDEX_URL: HTTPStatus.OK,
            self.POST_DETAIL_URL: HTTPStatus.OK,
            self.PROFILE_URL: HTTPStatus.OK,
            self.GROUP_URL: HTTPStatus.OK,
            CREATE_POST_URL: HTTPStatus.OK,
            self.POST_EDIT_URL: HTTPStatus.OK,
            UNEXISTING_URL: HTTPStatus.NOT_FOUND,
        }
        for client_url, status_code in client_url_status.items():
            with self.subTest(client_url=client_url):
                response = self.authorized_client.get(client_url)
                self.assertEqual(response.status_code, status_code)

    def test_urls_uses_correct_template_for_authorized_client(self):
        """
        URL-адрес соотвествует шаблону страницы для авторизованного клиента.
        """
        templates_url_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
            self.GROUP_URL: GROUP_TEMPLATE,
            CREATE_POST_URL: CREATE_POST_TEMPLATE,
            self.POST_EDIT_URL: CREATE_POST_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_urls_no_uses_template_for_guest_client(self):
        """URL-адрес не использует шаблон для не авторизованного клиента"""
        templates_url_names = {
            CREATE_POST_URL: CREATE_POST_TEMPLATE,
            self.POST_EDIT_URL: CREATE_POST_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateNotUsed(response, template)
