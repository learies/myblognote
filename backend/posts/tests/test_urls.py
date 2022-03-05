from http import HTTPStatus

from django.test import TestCase, Client

from posts.models import User, Post

AUTHOR = 'test_author'
POST_TITLE = 'Тестовый заголовок'
POST_TEXT = 'Тестовый техст поста'

INDEX_URL = '/'
INDEX_TEMPLATE = 'posts/index.html'

POST_DETAIL_TEMPLATE = 'posts/post_detail.html'


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

    def setUp(self):
        self.guest_client = Client()

    def test_index_status_page(self):
        """Доступность index страницы"""
        response = self.guest_client.get(INDEX_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_detail_status_page(self):
        """Доступность post_deatil страницы"""
        response = self.guest_client.get(self.POST_DETAIL_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес соотвествует шаблону страницы"""
        templates_url_names = {
            INDEX_URL: INDEX_TEMPLATE,
            self.POST_DETAIL_URL: POST_DETAIL_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
