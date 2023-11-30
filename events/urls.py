from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('events/', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/', views.event_registration, name='event_registration'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_event/', views.register_new_event, name='register_new_event'), 
]

urlpatterns += [
    path('api/events/', views.EventListAPIView.as_view(), name='event-list-api'),
    path('api/events/<int:event_id>/', views.EventDetailAPIView.as_view(), name='event-detail-api'),
    path('api/events/<int:event_id>/register/', views.UserRegistrationAPIView.as_view(), name='user-registration-api'),
    path('api/user/registrations/', views.UserRegisteredEventsAPIView.as_view(), name='user-registered-events-api'),
]
