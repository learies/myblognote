from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, User
from posts.tests.data_for_test import (AUTHOR, CREATE_POST_TEMPLATE,
                                       DESCRIPTION, GROUP_SLUG, GROUP_TEMPLATE,
                                       GROUP_TITLE, INDEX_TEMPLATE,
                                       POST_DETAIL_TEMPLATE, POST_TEXT,
                                       POST_TITLE, PROFILE_TEMPLATE)

INDEX = 'posts:index'
POST_DETAIL = 'posts:post_detail'
PROFALE = 'posts:profile'
GROUP_POSTS = 'posts:group_posts'
CREATE_POST = 'posts:post_create'
EDIT_POST = 'posts:post_edit'

LOGIN_URL = '/auth/login/?next=/create/'


class PostViewsTests(TestCase):
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
            group=cls.group,
        )
        cls.INDEX_URL = reverse(
            INDEX,
        )
        cls.POST_DETAIL_URL = reverse(
            POST_DETAIL,
            kwargs={'post_id': cls.post.id},
        )
        cls.PROFILE_URL = reverse(
            PROFALE,
            kwargs={'username': cls.user},
        )
        cls.GROUP_POSTS_URL = reverse(
            GROUP_POSTS,
            kwargs={'slug': cls.group.slug},
        )
        cls.CREATE_POST_URL = reverse(
            CREATE_POST,
        )
        cls.EDIT_POST_URL = reverse(
            EDIT_POST,
            kwargs={'post_id': cls.post.id},
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес соответствует шаблону страницы"""
        templates_pages_names = {
            self.INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
            self.GROUP_POSTS_URL: GROUP_TEMPLATE,
            self.CREATE_POST_URL: CREATE_POST_TEMPLATE,
            self.EDIT_POST_URL: CREATE_POST_TEMPLATE,
        }
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_pages_uses_redirect_for_guest_client(self):
        """
        Проверка переадрисации URL-адресов для не авторизованного пользователя.
        """
        redirect_urls = {
            self.CREATE_POST_URL: LOGIN_URL,
        }
        for url, redirect in redirect_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, redirect)

    def test_post_view_on_page(self):
        """"Отображение поста на страницах"""
        pages = (
            self.INDEX_URL,
            self.POST_DETAIL_URL,
            self.PROFILE_URL,
            self.GROUP_POSTS_URL,
        )
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertContains(response, self.post)
