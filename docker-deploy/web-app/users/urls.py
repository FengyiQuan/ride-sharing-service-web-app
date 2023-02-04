from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

from .views import viewUserInfo, viewDriverInfo, UserEditView, driverEditView, userRidesView, userDetailsOwnedRidesView, \
    userDetailsSharedRidesView, ownedRideEditView, sharedRideEditView

urlpatterns = [
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('register/', views.register, name='register'),
    path('register_driver/', views.register_driver, name='register_driver'),
    # path('profile/', views.profile, name='profile'),
    path('logout/', auth_view.LogoutView.as_view(), name="logout"),
    path('profile/', viewUserInfo, name="profile"),
    path('driverprofile/', viewDriverInfo, name="driverprofile"),
    path('editprofile/', UserEditView.as_view(), name="edituserprofile"),
    path('editdriverprofile/', driverEditView.as_view(), name="editdriverprofile"),
    path('user_rides/', userRidesView, name="user_rides"),
    path('user_owned_rides_detail/<int:id>/', userDetailsOwnedRidesView, name="user_owned_rides_detail"),
    path('user_shared_rides_detail/<int:id>/', userDetailsSharedRidesView, name="user_shared_rides_detail"),
    path('user_owned_rides_edit/<int:id>/', ownedRideEditView.as_view(), name="user_owned_rides_edit"),
    path('user_shared_rides_edit/<int:id>/', sharedRideEditView.as_view(), name="user_shared_rides_edit"),

]
