from .models import CustomUser
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UserMixin():
    pass


class UserDetailView(DetailView):
    model = CustomUser
    __fields__ = '__all__'
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        context['username'] = context['profile'].username
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
