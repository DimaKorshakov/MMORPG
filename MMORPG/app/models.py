from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    header = models.CharField(max_length=50, unique=True, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    text = CKEditor5Field('text', config_name='extends')
    email = models.EmailField()
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", default=True)

    def __str__(self):
        return f'{self.date} {self.header} {self.email} {self.cat}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def get_url(self):
        return reverse('new_comment', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['id']


class Comment(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)
    body = models.TextField(verbose_name="Текст", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.ForeignKey(User, verbose_name="Автор поста", blank=True, null=True, on_delete=models.CASCADE, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост", editable=True)
    status = models.BooleanField(default=False, verbose_name="Принять")
    email = models.EmailField()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('comment', kwargs={'comment_slug': self.slug})

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарий'
        ordering = ['created']

