from django.contrib.auth.urls import urlpatterns
from django.urls import path
from .views import UserCreateView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns += [
    path(route='auth/register/', view=UserCreateView.as_view(), name='registration'),
    path(route='auth/password_change', view=PasswordChangeView.as_view(), name='password_change'),
    path("auth/password_reset/", view=PasswordResetView.as_view(
        success_url=reverse_lazy("users:password_reset_done")), name="password_reset",
         ),
    path("auth/reset/<uidb64>/<token>/", view=PasswordResetConfirmView.as_view(
        success_url=reverse_lazy("users:password_reset_complete")), name="password_reset_confirm",
         ),
]
