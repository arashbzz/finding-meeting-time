from django.contrib import admin
from django.urls import path, include
from meeting_time import urls as meeting_app_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('meeting/', include(meeting_app_urls)),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)