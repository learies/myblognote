from http import HTTPStatus

from django.test import TestCase, Client

INDEX_URL = '/'
INDEX_TEMPLATE = 'posts/index.html'


class StaticURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_index_status_page(self):
        """Доступность index страницы"""
        response = self.guest_client.get(INDEX_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес соотвествует шаблону страницы"""
        templates_url_names = {
            INDEX_URL: INDEX_TEMPLATE,
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
