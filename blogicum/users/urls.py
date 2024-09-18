from django.contrib.auth.urls import urlpatterns
from django.http import HttpResponse
from django.urls import path

app_name = 'users'


def simple_view(request):
    return HttpResponse('<h1>REGISTER</h1>')


urlpatterns += [
    path(route='auth/register/', view=simple_view, name='register'),
    #    path(route='profile/<slug:username>/', view=simple_view, name='user_profile'),
]
