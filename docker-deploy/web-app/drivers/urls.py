from django.urls import path
from . import views

# from django.contrib.auth import views as auth_view

# from .forms import LoginForm

urlpatterns = [
    # path('', views.home, name='home'),

    # path('login/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    # path('register/', views.register, name='register'),
    path('ride_list/', views.ride_list, name='driver_ride_list'),
    # path('rides/', views.ride_list, name='ride_list'),
    # path('test/', views.show_all_ride_list, name='ride_list'),
    # # path('profile/', views.profile, name='profile'),
    # path('logout/', auth_view.LogoutView.as_view(), name="logout"),
]
