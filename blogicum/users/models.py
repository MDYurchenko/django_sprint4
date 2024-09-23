from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    '''
    Кастомная расширяемая модель пользователя.
    '''

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        print('in get absolute url')
        return reverse('blog:profile', kwargs={'username': self.username})
