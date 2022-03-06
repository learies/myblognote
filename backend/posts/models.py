from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
    )
    text = models.TextField(
        'Текст публикации',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='groups',
        verbose_name='Группа',
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = (
            '-pub_date',
        )

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        'Описание',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title
