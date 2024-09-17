from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import Category, Post
from django.utils import timezone
from django.views.generic import ListView

NUMBER_OF_POST_ON_INDEX_PAGE = 5


class PostListView(ListView):
    model = Post
    ordering = 'created_at'
    paginate_by = NUMBER_OF_POST_ON_INDEX_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_posts.get_published_posts()


def index(request: HttpRequest) -> HttpResponse:  # удалить, не используется
    """
    Функция для отображения главной страницы. На ней кратко отображена
    информация о последних постах.
    :param request: HttpRequest
    :return:
    """
    post_list = Post.published_posts.get_published_posts(

    ).order_by(
        'created_at'
    )[:NUMBER_OF_POST_ON_INDEX_PAGE]
    return render(request,
                  'blog/index.html',
                  context={'post_list': post_list},
                  status=200)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Функция для отображения подробной информации об одном посте.
    :param request: HttpRequest
    :param id: уникальный идентификатор поста, целое число.
    :return: HttpResponse
    """
    current_date = timezone.now()
    try:
        post = Post.objects.get(pk=post_id,
                                is_published=True,
                                category__is_published=True,
                                pub_date__lte=current_date,
                                )
        return render(request,
                      'blog/detail.html',
                      context={'post': post},
                      status=200)
    except Post.DoesNotExist:
        return HttpResponseNotFound('<h1>404 Page not found</h1>')
    # я не использовать  get_object_or_404 потому что,
    # возвращая HttpResponseNotFound
    # у меня как будто больше возможностей кастомизировать страинцу
    # с ответом
    # только вот ещё есть HttpResponseBadRequest со статус-кодом 400,
    # и как
    # будто мне бы добавить проверку на то, что передается в качестве
    # post_id:
    # если формат неверный, то вернуть 400, а если формат верный,
    # но такого поста - нет,
    # то вернуть 404. Но я не знаю: просто на принадлежность к int
    # проверить post_id или
    # как? pydantic с джангой используют? Или все моделях заложено?
    # Ещё не понял, как в менеджер передать post_id.
    # Для списка всех постов менеджер
    # написал.


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """
    Функция для отображения (в будущем) постов определенной категории.
    На данный момент функция-заглушка.
    :param request: HttpRequest
    :param category_slug: уникальный идентификатор категории постов
     в виде слага.
    :return: HttpResponse
    """
    try:
        category = Category.objects.filter(
            is_published=True
        ).get(slug=category_slug)

        post_list = Post.published_posts.get_published_posts().filter(
            category__slug=category_slug,
        ).order_by('created_at')

        return render(request,
                      'blog/category.html',
                      context={'post_list': post_list,
                               'category': category,
                               },
                      status=200)
    except Category.DoesNotExist:
        return HttpResponseNotFound('<h1>404 Page not found</h1>')
