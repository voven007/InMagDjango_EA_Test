from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns += doc_urls

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
    )
