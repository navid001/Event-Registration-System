# event_registration_system/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('events/', include('events.urls', namespace='events')),
    path('',include('events.urls'))
]
