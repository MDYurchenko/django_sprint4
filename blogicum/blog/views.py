from .models import Post, Comment, Category
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, \
    CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateCommentForm, CreatePostForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count
from django.http import Http404

NUMBER_OF_POST_ON_PAGE = 10


class PostListMixin(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = NUMBER_OF_POST_ON_PAGE


class PostListView(PostListMixin):
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_posts.get_published_posts(
        ).annotate(
            comment_count=Count("comments")
        ).order_by('-pub_date')


class CategoryPostList(PostListMixin):
    template_name = 'blog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return context

    def get_queryset(self):
        return Post.published_posts.get_published_posts().filter(
            category__slug=self.kwargs['category_slug'],
            category__is_published=True,
        ).annotate(
            comment_count=Count("comments")
        ).order_by('-pub_date')


class PostDetail(DetailView):
    model = Post
    fields = '__all__'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if (self.request.user != post.author) and (
                not post.is_published):
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateCommentForm()
        context["comments"] = (
            self.get_object(
            ).comments.select_related("post")
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={
                "username": self.request.user.username,
            },
        )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [
        'title',
        'text',
        'pub_date',
        'category',
        'location',
        'image',
        'is_published'
    ]
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if self.request.user != post.author:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/create.html"
    success_url = reverse_lazy("blog:index")
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if self.request.user != post.author:
            return redirect("blog:index")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreatePostForm(instance=self.object)
        return context


class BaseComment(LoginRequiredMixin):
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={"post_id": self.kwargs["post_id"]})


class CommentCreateView(BaseComment, CreateView):
    ...


class CommentEditUpdateView(BaseComment):
    pk_url_kwarg = "comment_id"
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        if self.request.user != comment.author:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class CommentUpdateView(CommentEditUpdateView, UpdateView):
    ...


class CommentDeleteView(CommentEditUpdateView, DeleteView):
    ...
