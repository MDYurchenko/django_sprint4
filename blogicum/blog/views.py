from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from .models import Category, Post, Comment
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import CreateCommentForm, CreatePostForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

NUMBER_OF_POST_ON_INDEX_PAGE = 5


class PostListView(ListView):
    model = Post
    ordering = 'created_at'
    paginate_by = NUMBER_OF_POST_ON_INDEX_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_posts.get_published_posts()


class CategoryPostList(ListView):
    model = Post
    ordering = 'created_at'
    paginate_by = NUMBER_OF_POST_ON_INDEX_PAGE
    template_name = 'blog/category.html'
    allow_empty = False

    def get_queryset(self):
        return Post.published_posts.get_published_posts().filter(category__slug=self.kwargs['category_slug'])


class PostDetail(DetailView):
    model = Post
    __fields__ = '__all__'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('blog:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["comments"] = (
            self.get_object().comments.prefetch_related("author").all()
        )
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = CreatePostForm
    __fields__ = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')


class PostUpdateView(UpdateView):
    model = Post
    __fields__ = '__all__'
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:post_detail')


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


class CommentCreateView(CreateView):
    model = Comment
    post = None
    form_class = CreateCommentForm

    # template_name = 'blog/includes/comments.html'

    def dispatch(self, request, *args, **kwargs):
        self.birthday = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.kwargs["post_id"]})


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CreateCommentForm
    post = None
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        print('in_dispatch')
        self.post = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.request.post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.post.pk})
