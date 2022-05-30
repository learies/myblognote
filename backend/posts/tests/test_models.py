from django.test import TestCase
from posts.models import Group, Post, User
from posts.tests.data_for_test import (AUTHOR, DESCRIPTION, GROUP_SLUG,
                                       GROUP_TITLE, PICTURE, POST_TEXT,
                                       POST_TITLE)


class PostModelTest(TestCase):
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
            image=PICTURE,
        )

    def test_post_verbose_name(self):
        """Поля Post verbose_name совпадает с ожидаемым"""
        field_verboses = {
            'title': 'Заголовок',
            'text': 'Текст публикации',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
            'image': 'Картинка',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_meta = self.post._meta.get_field(value).verbose_name
                self.assertEqual(verbose_meta, expected)

    def test_group_verbose_name(self):
        """Поля Group verbose_name совпадает с ожидаемым"""
        field_verboses = {
            'title': 'Название',
            'slug': 'Слаг',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                verbose_meta = self.group._meta.get_field(value).verbose_name
                self.assertEqual(verbose_meta, expected)

    def test_post_string_representation(self):
        """В модели Post значение поля __str__ отображается правильно"""
        expected_title = self.post.title
        self.assertEqual(expected_title, str(self.post))

    def test_group_string_representation(self):
        """В модели Grou значение поля __str__ отображается правильно"""
        expected_title = self.group.title
        self.assertEqual(expected_title, str(self.group))
