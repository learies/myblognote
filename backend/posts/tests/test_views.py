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
    GROUP_TITLE,
    GROUP_SLUG,
    DESCRIPTION,
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

    def test_post_view_on_page(self):
        """"Вывод поста на струницы"""
        pages = (
            INDEX_URL,
            self.POST_DETAIL_URL,
            self.PROFILE_URL,
            self.GROUP_POSTS_URL,
        )
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertContains(response, self.post)
