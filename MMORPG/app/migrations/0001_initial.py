# Generated by Django 4.2.2 on 2023-10-07 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категории',
                'verbose_name_plural': 'Категория',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('header', models.CharField(max_length=50, unique=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('text', django_ckeditor_5.fields.CKEditor5Field(verbose_name='text')),
                ('email', models.EmailField(max_length=254)),
                ('author', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.category', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('body', models.TextField(blank=True, null=True, verbose_name='Текст')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('status', models.BooleanField(default=False, verbose_name='Принять')),
                ('email', models.EmailField(max_length=254)),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор поста')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Комментарии',
                'verbose_name_plural': 'Комментарий',
                'ordering': ['created'],
            },
        ),
    ]
