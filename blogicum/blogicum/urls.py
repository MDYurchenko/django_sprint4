from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [path('admin/', admin.site.urls),
               path('pages/', include('pages.urls', namespace='pages')),
               path('', include('users.urls')),
               path('', include('django.contrib.auth.urls')),
               path('', include('blog.urls', namespace='blog')),
               ] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
