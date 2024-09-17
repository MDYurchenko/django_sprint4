# Generated by Django 3.2.16 on 2024-09-17 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


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
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Автоматически генерируемое поле.', verbose_name='Добавлено')),
                ('title', models.CharField(help_text='Укажите название категории публикаций (максимум 256 символов).', max_length=256, verbose_name='Заголовок')),
                ('description', models.TextField(help_text='Введите описание категории публикаций', verbose_name='Описание')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Автоматически генерируемое поле.', verbose_name='Добавлено')),
                ('name', models.CharField(help_text='Введите название местоположения (максимум 256 символов).', max_length=256, verbose_name='Название места')),
            ],
            options={
                'verbose_name': 'местоположение',
                'verbose_name_plural': 'Местоположения',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Автоматически генерируемое поле.', verbose_name='Добавлено')),
                ('title', models.CharField(help_text='Введите название публикации (максимум 256 символов).', max_length=256, verbose_name='Заголовок')),
                ('text', models.TextField(help_text='Введите текст публикации.', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('category', models.ForeignKey(help_text='Выберете категорию публикации (можно оставить без категории).', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category', verbose_name='Категория')),
                ('location', models.ForeignKey(blank=True, help_text='Укажите местоположение, связанное с публикацией.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.location', verbose_name='Местоположение')),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'Публикации',
            },
            managers=[
                ('published_posts', django.db.models.manager.Manager()),
            ],
        ),
    ]
