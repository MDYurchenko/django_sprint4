from .models import CustomUser
from blog.models import Post
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserMixin():
    pass


class UserDetailView(DetailView):
    model = CustomUser
    fields = '__all__'
    template_name = 'blog/profile.html'

    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        print('in context', kwargs)
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        if self.request.user.username == self.kwargs["username"]:
            context["page_obj"] = (
                self.get_object().posts.prefetch_related("author").all()
            )
        else:
            context["page_obj"] = (
                self.get_object().posts.prefetch_related("author").filter(is_published=True)
            )
        print(context['profile'].is_staff)
        return context


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('index')


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'blog/user.html'
    fields = (
        # 'username',
        'first_name',
        'last_name',
        'email',

    )

    def get_object(self):
        return self.request.user
