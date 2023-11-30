# events/urls.py

from django.urls import path
from . import views
# from views import event_list, event_detail, event_registration, user_dashboard

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
]
