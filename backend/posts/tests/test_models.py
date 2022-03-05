from django.test import TestCase

from posts.models import User, Post
from posts.tests.data_for_test import (
    AUTHOR,
    POST_TITLE,
    POST_TEXT,
)


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.post = Post.objects.create(
            title=POST_TITLE,
            text=POST_TEXT,
            author=cls.user,
        )

    def test_verbose_name(self):
        """Поля verbose_name совпадает с ожидаемым"""
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст публикации',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_meta = self.post._meta.get_field(value).verbose_name
                self.assertEqual(verbose_meta, expected)

    def test_post_string_representation(self):
        """В модели Post значение поля __str__ отображается правильно"""
        expected_title = self.post.title
        self.assertEqual(expected_title, str(self.post))
