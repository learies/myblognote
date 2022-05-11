from django.test import Client, TestCase
from django.urls import reverse
from posts.forms import PostForm
from posts.models import Comment, Group, Post, User
from posts.tests.data_for_test import (AUTHOR, DESCRIPTION, GROUP_SLUG,
                                       GROUP_TITLE, PICTURE, POST_TEXT,
                                       POST_TITLE)

CREATE_POST = 'posts:post_create'
PROFALE = 'posts:profile'
ADD_COMMENT = 'posts:add_comment'
POST_DETAIL = 'posts:post_detail'

POST_TITLE_TWO = 'Второй тестовый заголовок'
POST_TEXT_TWO = 'Второй тестовый текст поста'
COMMENT_TEXT = 'Новый комментарий'


class PostCreateFormTests(TestCase):
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
            image=PICTURE,
        )
        cls.CREATE_POST_URL = reverse(
            CREATE_POST,
        )
        cls.PROFILE_URL = reverse(
            PROFALE,
            kwargs={'username': cls.user},
        )
        cls.ADD_COMMENT_URL = reverse(
            ADD_COMMENT,
            kwargs={'post_id': cls.post.pk},
        )
        cls.POST_DETAIL_URL = reverse(
            POST_DETAIL,
            kwargs={'post_id': cls.post.pk},
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post"""
        posts_count = Post.objects.count()
        form_data = {
            'title': POST_TITLE_TWO,
            'text': POST_TEXT_TWO,
            'slug': GROUP_SLUG,
            'image': PICTURE,
        }
        response = self.authorized_client.post(
            self.CREATE_POST_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, self.PROFILE_URL)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                title=POST_TITLE_TWO,
                text=POST_TEXT_TWO,
            ).exists()
        )

    def test_create_comment(self):
        """Валидная форма создает запись в Comment."""
        comments_count = Comment.objects.count()
        form_data = {
            'text': COMMENT_TEXT,
        }
        response = self.authorized_client.post(
            self.ADD_COMMENT_URL,
            data=form_data,
            follow=True
        )
        comment = Comment.objects.first()
        self.assertRedirects(response, self.POST_DETAIL_URL)
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertTrue(
            Comment.objects.filter(
                post=self.post,
                text=COMMENT_TEXT,
                author=self.user,
            ).exists()
        )
