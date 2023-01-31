from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('request_ride/', views.request_ride, name='request_ride'),
    path('create_shared_request/', views.create_shared_request, name='shared_request'),
    path('ride_list/', views.user_ride_list, name='user_ride_list'),
    path('test/', views.show_all_ride_list, name='ride_list'),
]
