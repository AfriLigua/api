from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('elearning_platform.accounts.urls')),
    path('api/v1/', include('elearning_platform.courses.urls')),
    path('api/v1/', include('elearning_platform.bookings.urls')),
    path('api/v1/', include('elearning_platform.payments.urls')),
    path('api/v1/', include('elearning_platform.messaging.urls')),
    path('api/v1/', include('elearning_platform.notifications.urls')),
    path('api/v1/', include('elearning_platform.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
