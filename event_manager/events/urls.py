from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import EventViewSet, ReviewViewSet

app_name = 'events'

router = routers.DefaultRouter()
router.register(r'api/events', EventViewSet)
router.register(r'api/reviews', ReviewViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete_event'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='events/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/events/', views.api_event_list, name='api_event_list'),
    path('api/events/<int:pk>/', views.api_event_detail, name='api_event_detail'),
] + router.urls