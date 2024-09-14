# Generated by Django 3.2.16 on 2024-08-28 15:14

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now=True, help_text='#', verbose_name='Добавлено')),
                ('title', models.CharField(help_text='#', max_length=256, verbose_name='#')),
                ('description', models.TextField(help_text='#', verbose_name='Описание')),
                ('slug', models.SlugField(help_text='Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.', unique=True, verbose_name='Идентификатор')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now=True, help_text='#', verbose_name='Добавлено')),
                ('name', models.CharField(help_text='#', max_length=256, verbose_name='Название места')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=True, help_text='Снимите галочку, чтобы скрыть публикацию.', verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(auto_now=True, help_text='#', verbose_name='Добавлено')),
                ('title', models.CharField(help_text='#', max_length=256, verbose_name='Заголовок')),
                ('text', models.TextField(help_text='#', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(help_text='Если установить дату и время в будущем — можно делать отложенные публикации.', verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(help_text='#', on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
                ('category', models.ForeignKey(help_text='#', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='blog.category', verbose_name='Категория')),
                ('location', models.ForeignKey(blank=True, help_text='#', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='blog.location', verbose_name='Местоположение')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdmin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CategoryAdmin',
            fields=[
                ('category_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.category')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.category',),
        ),
        migrations.CreateModel(
            name='LocationAdmin',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.location')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.location',),
        ),
        migrations.CreateModel(
            name='PostAdmin',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.post')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.post',),
        ),
    ]