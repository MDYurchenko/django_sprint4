from django.contrib.auth.urls import urlpatterns
from django.urls import path
from .views import UserCreateView

app_name = 'users'

urlpatterns += [
    path(route='auth/register/', view=UserCreateView.as_view(), name='registration'),
]
