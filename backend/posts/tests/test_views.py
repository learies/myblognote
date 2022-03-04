from django.test import TestCase, Client
from django.urls import reverse

INDEX_URL = reverse('posts:index')
INDEX_TEMPLATE = 'posts/index.html'


class PostViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_pages_uses_correct_template(self):
        """URL-адрес соответствуюет шаблону страницы"""
        templates_pages_names = {
            INDEX_URL: INDEX_TEMPLATE
        }
        for url, template in templates_pages_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
