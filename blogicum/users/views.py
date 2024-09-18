from .models import CustomUser
from django.views.generic import CreateView, DetailView, UpdateView


class UserDetailView(DetailView):
    model = CustomUser
    __fields__ = '__all__'
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'registration/registration_form.html'


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'blog/user.html'
