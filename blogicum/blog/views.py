from .models import Post, Comment
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateCommentForm, CreatePostForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

NUMBER_OF_POST_ON_PAGE = 5


class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    paginate_by = NUMBER_OF_POST_ON_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.published_posts.get_published_posts()


class CategoryPostList(ListView):
    model = Post
    ordering = '-created_at'
    paginate_by = NUMBER_OF_POST_ON_PAGE
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


class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    form_class = CreatePostForm
    __fields__ = '__all__'
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={
                "username": self.request.user.username,
            },
        )


class PostUpdateView(UpdateView, LoginRequiredMixin):
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
    success_url = reverse_lazy('blog:post_detail')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreatePostForm(instance=self.object)
        return context


class CommentCreateView(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CreateCommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})


class CommentUpdateView(UpdateView, LoginRequiredMixin):
    model = Comment
    form_class = CreateCommentForm
    pk_url_kwarg = "comment_id"
    template_name = 'blog/comment.html'

    def form_valid(self, form):
        print('in form is valid')
        form.instance.comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.kwargs["post_id"]})

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        print(self.kwargs)
        if self.request.user != comment.author:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().delete(request, *args, **kwargs)
