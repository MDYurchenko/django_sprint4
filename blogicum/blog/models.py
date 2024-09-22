from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from users.models import CustomUser

MAX_TITLE_LENGHT = 256

User = get_user_model()


class PostListManager(models.Manager):
    def get_published_posts(self):
        current_date = timezone.now()
        posts_list = super().get_queryset().filter(
            pub_date__lte=current_date,
            is_published=True,
            category__is_published=True,
        ).all()
        return posts_list


class BaseModel(models.Model):
    is_published = models.BooleanField(
        null=False,
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
        verbose_name='Добавлено',
        help_text='Автоматически генерируемое поле.'
    )

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        blank=False,
        null=False,
        verbose_name='Заголовок',
        help_text='Введите название публикации (максимум 256 символов).',
    )
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='Текст',
        help_text='Введите текст публикации.',
    )
    pub_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время'
                  ' в будущем — можно делать отложенные публикации.',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=False,
        null=True,
        verbose_name='Категория',
        help_text='Выберете категорию публикации '
                  '(можно оставить без категории).',
    )
    author = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts',
        blank=False,
        null=False,
        verbose_name='Автор публикации',
        help_text='',
    )
    location = models.ForeignKey(
        to='Location',
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Местоположение',
        help_text='Укажите местоположение, связанное с публикацией.',
    )
    image = models.ImageField(
        'Изображение', upload_to='post_images', blank=True
    )

    published_posts = PostListManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'post_id': self.pk})


class Category(BaseModel):
    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        blank=False,
        null=False,
        verbose_name='Заголовок',
        help_text='Укажите название категории публикаций'
                  ' (максимум 256 символов).',

    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание',
        help_text='Введите описание категории публикаций',

    )
    slug = models.SlugField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены'
                  ' символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        blank=False,
        null=False,
        verbose_name='Название места',
        help_text='Введите название местоположения (максимум 256 символов).',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(models.Model):
    text = models.TextField(blank=False,
                            null=False,
                            verbose_name='Текст комментария',
                            help_text='Введите комментарий',
                            )
    author = models.ForeignKey(to=CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               blank=False,
                               null=False,
                               verbose_name='Автор комментария',
                               )
    post = models.ForeignKey(to=Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             blank=False,
                             null=False,
                             verbose_name='Комментируемый пост',
                             )
    created_at = models.DateTimeField(blank=False,
                                      null=False,
                                      auto_now_add=True,
                                      verbose_name='Добавлено',
                                      help_text='Автоматически генерируемое поле.')

    class Meta:
        ordering = ('created_at',)
