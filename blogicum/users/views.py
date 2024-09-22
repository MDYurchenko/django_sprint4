from .models import CustomUser
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from blog.views import NUMBER_OF_POST_ON_PAGE


class UserMixin():
    pass


class UserDetailView(DetailView):
    model = CustomUser
    fields = '__all__'
    template_name = 'blog/profile.html'

    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        page = self.request.GET.get('page', 1)
        if self.request.user.username == self.kwargs["username"]:
            context["page_obj"] = (
                Paginator(
                    self.get_object().posts.prefetch_related("author").all(),
                    NUMBER_OF_POST_ON_PAGE,
                ).get_page(page)
            )
        else:
            context["page_obj"] = (
                Paginator(
                    self.get_object().posts.prefetch_related("author").filter(
                        pub_date__lte=timezone.now(),
                        is_published=True,
                        category__is_published=True, )
                    ,
                    NUMBER_OF_POST_ON_PAGE,
                ).get_page(page)
            )
        return context


class UserCreateView(CreateView, LoginRequiredMixin):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('index')


class UserUpdateView(UpdateView, LoginRequiredMixin):
    model = CustomUser
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',

    )

    def get_object(self):
        return self.request.user
