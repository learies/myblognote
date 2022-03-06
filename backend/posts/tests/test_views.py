from django.test import TestCase, Client
from django.urls import reverse

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

INDEX_URL = reverse('posts:index')

POST_DETAIL = 'posts:post_detail'
PROFALE = 'posts:profile'
GROUP_POSTS = 'posts:group_posts'


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            title=POST_TITLE,
            text=POST_TEXT,
            author=cls.user,
            group=cls.group,
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

    def setUp(self):
        self.guest_client = Client()

    def test_pages_uses_correct_template(self):
        """URL-адрес соответствуюет шаблону страницы"""
        templates_pages_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
            self.PROFILE_URL: PROFILE_TEMPLATE,
            self.GROUP_POSTS_URL: GROUP_TEMPLATE,
        }
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_index_page(self):
        """Главная страница"""
        response = self.guest_client.get(INDEX_URL)
        self.assertContains(response, self.post)

    def test_post_detail_page(self):
        """Страница с постом"""
        response = self.guest_client.get(self.POST_DETAIL_URL)
        self.assertContains(response, self.post)

    def test_profile_page(self):
        """Страница профиля автора"""
        response = self.guest_client.get(self.PROFILE_URL)
        self.assertContains(response, self.post)

    def test_group_posts_page(self):
        """Страница группы с постами"""
        response = self.guest_client.get(self.GROUP_POSTS_URL)
        self.assertContains(response, self.post)
